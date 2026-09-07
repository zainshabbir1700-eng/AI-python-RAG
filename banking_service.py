import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
load_dotenv()

from kyc import kyc_router

app = FastAPI(title="Banking Risk, RAG & Reconciliation Service")
app.include_router(kyc_router)

# Mount local uploads directory for document access
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

DATABASE_URL = os.getenv("DATABASE_URL", "")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# ---------------------------------------------------------
# RULE #17 & #30: Deterministic Nightly Reconciliation
# ---------------------------------------------------------
@app.post("/api/reconciliation/run-nightly")
def run_nightly_reconciliation():
    conn = get_db()
    cur = conn.cursor()
    try:
        # Step 1: Ledger entries ka sum nikalna vs accounts ka reported balance
        cur.execute("""
            select 
                a.id as account_id,
                a.account_number,
                a.ledger_balance as reported_balance,
                coalesce(sum(case when le.direction = 'CREDIT' then le.amount else -le.amount end), 0) as calculated_balance
            from accounts a
            left join ledger_entries le on a.id = le.account_id
            group by a.id, a.account_number, a.ledger_balance;
        """)
        accounts = cur.fetchall()

        discrepancies = []
        for acc in accounts:
            diff = acc["reported_balance"] - acc["calculated_balance"]
            if abs(diff) > 0.001:  # Inconsistency detected
                discrepancies.append({
                    "account_id": str(acc["account_id"]),
                    "account_number": acc["account_number"],
                    "reported": float(acc["reported_balance"]),
                    "calculated": float(acc["calculated_balance"]),
                    "difference": float(diff)
                })

        status = "DISCREPANCY" if discrepancies else "PASSED"

        # Record reconciliation run result
        cur.execute("""
            insert into reconciliation_runs (run_date, started_at, completed_at, status, accounts_checked, discrepancies_found, details)
            values (current_date, now(), now(), %s, %s, %s, %s::jsonb)
            returning id;
        """, (status, len(accounts), len(discrepancies), psycopg2.extras.Json(discrepancies)))
        
        conn.commit()
        return {
            "status": status,
            "accounts_checked": len(accounts),
            "discrepancies_count": len(discrepancies),
            "discrepancies": discrepancies
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# RULE #18, #19, #24: RAG Draft Generation (No Hallucination)
# ---------------------------------------------------------
class SupportQuery(BaseModel):
    case_id: str
    customer_query: str

@app.post("/api/rag/generate-draft")
def generate_support_draft(req: SupportQuery):
    conn = get_db()
    cur = conn.cursor()
    try:
        # Mock policy check (Pinecone integration point)
        query_text = req.customer_query.lower()
        
        # Guardrail: Agar policy relevant nahi hai to hallucinate na kare
        if "card" in query_text or "decline" in query_text:
            draft = "Your card was declined due to either insufficient funds or temporary security threshold. Please check your daily limits in the mobile portal."
            guardrail_status = "PASSED"
        elif "limit" in query_text:
            draft = "Minor accounts have a strict 50% daily limit. Transactions exceeding this threshold require guardian sign-off."
            guardrail_status = "PASSED"
        else:
            draft = "NO_SUPPORTED_POLICY: Query could not be verified against official banking guidelines. Escalated for human review."
            guardrail_status = "FALLBACK"

        # Save draft in database (Rule #18: Draft only)
        cur.execute("""
            insert into rag_drafts (support_case_id, draft_text, guardrail_status, approval_status, confidence)
            values (%s, %s, %s, 'PENDING', 0.95)
            returning id;
        """, (req.case_id, draft, guardrail_status))
        
        draft_id = cur.fetchone()["id"]
        conn.commit()

        return {
            "status": "SUCCESS",
            "draft_id": str(draft_id),
            "guardrail_status": guardrail_status
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()