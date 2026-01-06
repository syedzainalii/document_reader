from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class StudentBase(BaseModel):
    """Base schema for student data."""
    student_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    program: Optional[str] = None
    year_of_study: Optional[str] = None
    document_type: Optional[str] = None


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    extracted_text: Optional[str] = None
    original_image_path: Optional[str] = None
    photo_path: Optional[str] = None
    processed_image_path: Optional[str] = None


class StudentUpdate(BaseModel):
    """Schema for updating student data."""
    student_id: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    program: Optional[str] = None
    year_of_study: Optional[str] = None
    document_type: Optional[str] = None


class StudentResponse(StudentBase):
    """Schema for student response."""
    id: int
    extracted_text: Optional[str] = None
    original_image_path: Optional[str] = None
    photo_path: Optional[str] = None
    processed_image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudentSearchResponse(BaseModel):
    """Schema for search results."""
    total: int
    page: int
    page_size: int
    students: list[StudentResponse]


class OCRResult(BaseModel):
    """Schema for OCR processing result."""
    success: bool
    extracted_text: Optional[str] = None
    student_data: Optional[dict] = None
    photo_extracted: bool = False
    error: Optional[str] = None


class UploadResponse(BaseModel):
    """Schema for upload response."""
    success: bool
    message: str
    student: Optional[StudentResponse] = None
    ocr_result: Optional[OCRResult] = None
