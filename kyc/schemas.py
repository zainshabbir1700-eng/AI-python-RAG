import re
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator


CNIC_REGEX = re.compile(r"^\d{5}-\d{7}-\d{1}$")
PHONE_REGEX = re.compile(r"^\+923\d{9}$")


class KYCFormValidation(BaseModel):
    kyc_token: str = Field(..., min_length=1, description="Unique verification token provided to the customer")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full Name as printed on CNIC")
    cnic: str = Field(..., description="CNIC in format 00000-0000000-0")
    phone: str = Field(..., description="Pakistani mobile phone in format +923XXXXXXXXX")
    dob: str = Field(..., description="Date of Birth in YYYY-MM-DD format")
    address: str = Field(..., min_length=5, max_length=500, description="Residential Address")

    @field_validator("cnic")
    @classmethod
    def validate_cnic(cls, v: str) -> str:
        clean_cnic = v.strip()
        # Handle unhyphenated 13 digits by formatting
        digits_only = re.sub(r"\D", "", clean_cnic)
        if len(digits_only) == 13 and "-" not in clean_cnic:
            clean_cnic = f"{digits_only[:5]}-{digits_only[5:12]}-{digits_only[12]}"
        
        if not CNIC_REGEX.match(clean_cnic):
            raise ValueError("CNIC must follow the official Pakistani format: 00000-0000000-0")
        return clean_cnic

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        clean_phone = v.strip().replace(" ", "").replace("-", "")
        # Automatically normalize 03XXXXXXXXX to +923XXXXXXXXX
        if clean_phone.startswith("03") and len(clean_phone) == 11:
            clean_phone = "+92" + clean_phone[1:]
        elif clean_phone.startswith("923") and len(clean_phone) == 12:
            clean_phone = "+" + clean_phone
        elif clean_phone.startswith("00923") and len(clean_phone) == 14:
            clean_phone = "+" + clean_phone[2:]

        if not PHONE_REGEX.match(clean_phone):
            raise ValueError("Mobile phone number must be a valid Pakistani mobile: +923XXXXXXXXX")
        return clean_phone

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        clean_dob = v.strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", clean_dob):
            raise ValueError("Date of Birth must be in YYYY-MM-DD format")
        return clean_dob


class OCRVerificationResult(BaseModel):
    engine: str
    status: str
    extracted_cnic: Optional[str] = None
    cnic_matched: bool = False
    name_matched: bool = False
    confidence: float = 0.0
    details: str


class KYCSubmitSuccessResponse(BaseModel):
    status: str = "SUCCESS"
    message: str = "KYC verified successfully. Account is now ACTIVE with PKR 100 bonus credited!"
    account_status: str = "ACTIVE"
    bonus_credited: bool = True
    bonus_amount_pkr: float = 100.00
    kyc_token: str
    cnic: str
    doc_url: str
    selfie_url: str
    ocr: OCRVerificationResult
    rpc_result: Optional[Any] = None


class KYCErrorResponse(BaseModel):
    status: str = "ERROR"
    detail: str
    code: str = "KYC_SUBMISSION_FAILED"
    validation_errors: Optional[Dict[str, Any]] = None
