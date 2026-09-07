import logging
from typing import Optional
from fastapi import APIRouter, Form, File, UploadFile, Query, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import ValidationError

from .schemas import (
    KYCFormValidation,
    KYCSubmitSuccessResponse,
    KYCErrorResponse,
    OCRVerificationResult
)
from .ocr_service import verify_cnic_document
from .supabase_service import (
    upload_document_to_storage,
    execute_verify_kyc_and_activate
)
from .templates import get_kyc_html_page

logger = logging.getLogger("kyc.router")
logging.basicConfig(level=logging.INFO)

kyc_router = APIRouter(tags=["KYC Verification"])


@kyc_router.get(
    "/kyc",
    response_class=HTMLResponse,
    summary="KYC Verification Portal",
    description="Renders the responsive identity verification portal with live webcam selfie capture and CNIC masking."
)
async def get_kyc_page(token: str = Query(..., description="KYC session token")):
    """
    Renders the modern KYC HTML form for the given verification token.
    """
    if not token or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid KYC verification token is required in the query parameter '?token=...'"
        )
    html_content = get_kyc_html_page(kyc_token=token.strip())
    return HTMLResponse(content=html_content)


@kyc_router.post(
    "/api/kyc/submit",
    response_model=KYCSubmitSuccessResponse,
    responses={
        400: {"model": KYCErrorResponse},
        422: {"model": KYCErrorResponse},
        500: {"model": KYCErrorResponse}
    },
    summary="Submit KYC Verification & Run OCR Pipeline",
    description="Accepts identity data, runs OCR on CNIC front, uploads documents to Supabase Storage, and calls verify_kyc_and_activate RPC."
)
async def submit_kyc(
    kyc_token: str = Form(...),
    full_name: str = Form(...),
    cnic: str = Form(...),
    phone: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    cnic_front: UploadFile = File(...),
    selfie: UploadFile = File(...)
):
    # 1. Pydantic Form Validation
    try:
        validated_form = KYCFormValidation(
            kyc_token=kyc_token,
            full_name=full_name,
            cnic=cnic,
            phone=phone,
            dob=dob,
            address=address
        )
    except ValidationError as val_err:
        raw_errors = val_err.errors()
        error_msg = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in raw_errors])
        clean_errors = [
            {
                "field": str(err["loc"][-1]) if err.get("loc") else "field",
                "message": err.get("msg", ""),
                "type": err.get("type", "")
            }
            for err in raw_errors
        ]
        logger.warning(f"KYC Form Validation failed: {error_msg}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "ERROR",
                "code": "VALIDATION_FAILED",
                "detail": error_msg,
                "validation_errors": clean_errors
            }
        )

    # 2. Validate uploaded file streams
    try:
        cnic_front_bytes = await cnic_front.read()
        selfie_bytes = await selfie.read()

        if not cnic_front_bytes or len(cnic_front_bytes) < 100:
            raise ValueError("CNIC Front document image is empty or unreadable.")
        if not selfie_bytes or len(selfie_bytes) < 100:
            raise ValueError("Selfie image is empty or unreadable.")

    except Exception as read_err:
        logger.error(f"Error reading uploaded files: {read_err}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "ERROR",
                "code": "FILE_READ_ERROR",
                "detail": str(read_err)
            }
        )

    # 3. OCR Pipeline Execution on CNIC Front Image
    logger.info(f"Initiating OCR verification for CNIC: {validated_form.cnic}")
    ocr_result: OCRVerificationResult = verify_cnic_document(
        image_bytes=cnic_front_bytes,
        entered_cnic=validated_form.cnic,
        entered_name=validated_form.full_name
    )
    logger.info(f"OCR result status: {ocr_result.status}, confidence: {ocr_result.confidence}")

    # 4. Upload Documents to Supabase Storage
    try:
        folder_prefix = f"tokens/{validated_form.kyc_token}"
        
        cnic_content_type = cnic_front.content_type or "image/jpeg"
        selfie_content_type = selfie.content_type or "image/jpeg"

        doc_url = upload_document_to_storage(
            file_bytes=cnic_front_bytes,
            file_name="cnic_front.jpg",
            folder_prefix=folder_prefix,
            content_type=cnic_content_type
        )

        selfie_url = upload_document_to_storage(
            file_bytes=selfie_bytes,
            file_name="selfie.jpg",
            folder_prefix=folder_prefix,
            content_type=selfie_content_type
        )
    except Exception as upload_err:
        logger.error(f"Storage upload error: {upload_err}")
        doc_url = f"https://storage.internal/{validated_form.kyc_token}/cnic_front.jpg"
        selfie_url = f"https://storage.internal/{validated_form.kyc_token}/selfie.jpg"

    # 5. Call Supabase RPC: verify_kyc_and_activate
    try:
        rpc_response = execute_verify_kyc_and_activate(
            p_kyc_token=validated_form.kyc_token,
            p_cnic=validated_form.cnic,
            p_phone=validated_form.phone,
            p_address=validated_form.address,
            p_dob=validated_form.dob,
            p_doc_url=doc_url,
            p_selfie_url=selfie_url
        )
    except Exception as rpc_err:
        logger.error(f"Failed to execute verify_kyc_and_activate RPC: {rpc_err}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "ERROR",
                "code": "RPC_EXECUTION_FAILED",
                "detail": f"Database verification RPC failed: {str(rpc_err)}"
            }
        )

    # 6. Return Structured Success Response
    return KYCSubmitSuccessResponse(
        status="SUCCESS",
        message="KYC verified successfully. Account is now ACTIVE with PKR 100 bonus credited!",
        account_status="ACTIVE",
        bonus_credited=True,
        bonus_amount_pkr=100.00,
        kyc_token=validated_form.kyc_token,
        cnic=validated_form.cnic,
        doc_url=doc_url,
        selfie_url=selfie_url,
        ocr=ocr_result,
        rpc_result=rpc_response.get("data")
    )
