import io
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient
from banking_service import app
from kyc.schemas import KYCFormValidation
from kyc.ocr_service import verify_cnic_document

client = TestClient(app)


def create_dummy_image(text: str = "42101-1234567-1") -> bytes:
    """Create an in-memory test image with text."""
    img = Image.new("RGB", (300, 150), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.text((20, 50), text, fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_kyc_get_page_success():
    """Verify GET /kyc?token=... returns 200 and renders complete HTML portal."""
    response = client.get("/kyc?token=TEST_TOKEN_XYZ_123")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text

    # Verify key form elements
    assert "TEST_TOKEN_XYZ_123" in html
    assert "name=\"kyc_token\"" in html
    assert "name=\"full_name\"" in html
    assert "name=\"cnic\"" in html
    assert "name=\"phone\"" in html
    assert "name=\"dob\"" in html
    assert "name=\"address\"" in html
    assert "name=\"cnic_front\"" in html
    assert "name=\"selfie\"" in html

    # Verify PKR 100 bonus mention and security
    assert "PKR 100" in html
    assert "SSL 256-Bit" in html
    assert "Webcam" in html


def test_kyc_get_page_missing_token():
    """Verify GET /kyc without token parameter returns 422 Unprocessable Entity."""
    response = client.get("/kyc")
    assert response.status_code == 422


def test_kyc_schema_validations():
    """Verify CNIC and Phone validation rules and normalizations."""
    # 1. Valid inputs
    valid_data = {
        "kyc_token": "TOK_001",
        "full_name": "Muhammad Zain",
        "cnic": "42101-1234567-1",
        "phone": "+923001234567",
        "dob": "1998-05-15",
        "address": "Gulshan-e-Iqbal, Karachi"
    }
    validated = KYCFormValidation(**valid_data)
    assert validated.cnic == "42101-1234567-1"
    assert validated.phone == "+923001234567"

    # 2. Auto-formatting of raw 13 digit CNIC
    unformatted = valid_data.copy()
    unformatted["cnic"] = "4210112345671"
    validated2 = KYCFormValidation(**unformatted)
    assert validated2.cnic == "42101-1234567-1"

    # 3. Auto-normalization of phone from 03XXXXXXXXX to +923XXXXXXXXX
    local_phone = valid_data.copy()
    local_phone["phone"] = "03001234567"
    validated3 = KYCFormValidation(**local_phone)
    assert validated3.phone == "+923001234567"

    # 4. Invalid CNIC format should raise ValueError
    invalid_cnic = valid_data.copy()
    invalid_cnic["cnic"] = "12345-invalid-1"
    failed = False
    try:
        KYCFormValidation(**invalid_cnic)
    except Exception:
        failed = True
    assert failed, "Invalid CNIC did not trigger validation error"

    # 5. Invalid Phone should raise ValueError
    invalid_phone = valid_data.copy()
    invalid_phone["phone"] = "+15551234567"
    failed_phone = False
    try:
        KYCFormValidation(**invalid_phone)
    except Exception:
        failed_phone = True
    assert failed_phone, "Invalid Phone did not trigger validation error"


def test_ocr_verification_resilience():
    """Verify OCR handles images and applies graceful fallback without crashing."""
    img_bytes = create_dummy_image("42101-1234567-1")
    result = verify_cnic_document(
        image_bytes=img_bytes,
        entered_cnic="42101-1234567-1",
        entered_name="Muhammad Zain"
    )
    assert result.status in ["VERIFIED", "LOW_CONFIDENCE_PASSED", "FALLBACK_ENGINE_UNAVAILABLE", "FALLBACK_OCR_EXECUTION_ERROR"]
    assert result.cnic_matched is True
    assert result.confidence > 0.0


def test_kyc_submit_endpoint_success():
    """Verify POST /api/kyc/submit with multipart data returns activation and PKR 100 bonus."""
    cnic_bytes = create_dummy_image("42101-1234567-1")
    selfie_bytes = create_dummy_image("Selfie Face")

    form_fields = {
        "kyc_token": "KYC_TEST_TOKEN_2026",
        "full_name": "Muhammad Zain",
        "cnic": "42101-1234567-1",
        "phone": "+923001234567",
        "dob": "1998-05-15",
        "address": "House 123, Street 4, Islamabad"
    }

    files = {
        "cnic_front": ("cnic_front.jpg", cnic_bytes, "image/jpeg"),
        "selfie": ("selfie.jpg", selfie_bytes, "image/jpeg")
    }

    response = client.post("/api/kyc/submit", data=form_fields, files=files)
    assert response.status_code == 200
    data = response.json()

    # Verify contract
    assert data["status"] == "SUCCESS"
    assert data["account_status"] == "ACTIVE"
    assert data["bonus_credited"] is True
    assert data["bonus_amount_pkr"] == 100.00
    assert data["kyc_token"] == "KYC_TEST_TOKEN_2026"
    assert data["cnic"] == "42101-1234567-1"
    assert "doc_url" in data
    assert "selfie_url" in data
    assert "ocr" in data
    assert data["ocr"]["cnic_matched"] is True


def test_kyc_submit_endpoint_validation_failure():
    """Verify POST /api/kyc/submit returns 422 if invalid CNIC is submitted."""
    cnic_bytes = create_dummy_image()
    selfie_bytes = create_dummy_image()

    form_fields = {
        "kyc_token": "KYC_TEST_TOKEN_2026",
        "full_name": "Muhammad Zain",
        "cnic": "invalid-cnic",
        "phone": "+923001234567",
        "dob": "1998-05-15",
        "address": "Islamabad"
    }

    files = {
        "cnic_front": ("cnic_front.jpg", cnic_bytes, "image/jpeg"),
        "selfie": ("selfie.jpg", selfie_bytes, "image/jpeg")
    }

    response = client.post("/api/kyc/submit", data=form_fields, files=files)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "ERROR"
    assert data["code"] == "VALIDATION_FAILED"


def test_existing_endpoints_unbroken():
    """Verify that existing RAG and Reconciliation endpoints continue functioning."""
    from unittest.mock import patch, MagicMock
    import banking_service

    # Verify routes registered in OpenAPI
    schema = app.openapi()
    paths = schema.get("paths", {})
    assert "/api/rag/generate-draft" in paths
    assert "/api/reconciliation/run-nightly" in paths
    assert "/kyc" in paths
    assert "/api/kyc/submit" in paths

    # Test RAG generate draft endpoint with mocked DB to prevent external network timeout
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = {"id": 101}
    mock_conn.cursor.return_value = mock_cur

    with patch.object(banking_service, "get_db", return_value=mock_conn):
        rag_payload = {
            "case_id": "CASE-999",
            "customer_query": "Why was my debit card declined?"
        }
        res = client.post("/api/rag/generate-draft", json=rag_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "SUCCESS"
        assert data["guardrail_status"] == "PASSED"
        assert data["draft_id"] == "101"


if __name__ == "__main__":
    tests = [
        test_kyc_get_page_success,
        test_kyc_get_page_missing_token,
        test_kyc_schema_validations,
        test_ocr_verification_resilience,
        test_kyc_submit_endpoint_success,
        test_kyc_submit_endpoint_validation_failure,
        test_existing_endpoints_unbroken,
    ]
    passed = 0
    print("=" * 60)
    print("RUNNING KYC MODULE TEST SUITE")
    print("=" * 60)
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {t.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print("=" * 60)
    print(f"RESULTS: {passed}/{len(tests)} TESTS PASSED")
    print("=" * 60)
    if passed != len(tests):
        exit(1)

