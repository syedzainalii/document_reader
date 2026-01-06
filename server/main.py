from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import shutil
from datetime import datetime, timedelta

from config import get_settings
from database import get_db, init_db, engine, Base
from models import Student
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentSearchResponse,
    UploadResponse,
    OCRResult
)
from schemas_auth import LoginRequest, TokenResponse, UserResponse
from auth import authenticate_admin, create_access_token, require_admin, get_current_user

# Try to import OCR service, but allow server to run without it
try:
    from services.ocr_service import OCRService
    OCR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OCR service not available: {e}")
    OCR_AVAILABLE = False
    OCRService = None

from services.excel_service import ExcelService

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(",") if settings.allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.upload_dir, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NED University Document Management System API",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Admin login endpoint.
    Returns JWT token for authenticated admin.
    """
    # Authenticate admin
    if not authenticate_admin(login_data.username, login_data.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": login_data.username, "role": "admin"},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information."""
    return UserResponse(
        username=current_user.get("sub"),
        role=current_user.get("role")
    )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Upload and process a student document.
    Extracts text and photo using OCR, stores data in database.
    """
    try:
        # Validate file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.pdf', '.tiff', '.bmp'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Create temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"temp_{timestamp}_{file.filename}"
        temp_path = os.path.join(settings.upload_dir, temp_filename)
        
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document with OCR
        if not OCR_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="OCR service is not available. Please install required dependencies (opencv-python-headless, pytesseract)"
            )
        
        ocr_result = OCRService.process_document(temp_path, settings.upload_dir)
        
        if not ocr_result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"OCR processing failed: {ocr_result.get('error', 'Unknown error')}"
            )
        
        # Extract student data
        student_data = ocr_result.get('student_data', {})
        
        # Validate required fields
        if not student_data.get('student_id') or not student_data.get('full_name'):
            # If OCR couldn't extract required fields, generate placeholder
            student_data['student_id'] = student_data.get('student_id') or f"UNKNOWN_{timestamp}"
            student_data['full_name'] = student_data.get('full_name') or "Unknown Student"
        
        # Create organized file structure
        student_dir = os.path.join(settings.upload_dir, student_data['student_id'])
        os.makedirs(student_dir, exist_ok=True)
        
        # Move files to student directory
        final_image_path = os.path.join(student_dir, f"document_{timestamp}{file_ext}")
        shutil.move(temp_path, final_image_path)
        
        photo_path = None
        if ocr_result.get('photo_path'):
            photo_filename = f"photo_{timestamp}.jpg"
            photo_path = os.path.join(student_dir, photo_filename)
            shutil.move(ocr_result['photo_path'], photo_path)
        
        # Check if student already exists
        existing_student = db.query(Student).filter(
            Student.student_id == student_data['student_id']
        ).first()
        
        if existing_student:
            # Update existing student
            for key, value in student_data.items():
                if value:
                    setattr(existing_student, key, value)
            
            existing_student.original_image_path = final_image_path
            if photo_path:
                existing_student.photo_path = photo_path
            existing_student.extracted_text = ocr_result.get('extracted_text')
            
            db.commit()
            db.refresh(existing_student)
            student = existing_student
            message = "Student data updated successfully"
        else:
            # Create new student
            student = Student(
                student_id=student_data['student_id'],
                full_name=student_data['full_name'],
                email=student_data.get('email'),
                phone=student_data.get('phone'),
                department=student_data.get('department'),
                program=student_data.get('program'),
                year_of_study=student_data.get('year_of_study'),
                document_type="ID Card",
                extracted_text=ocr_result.get('extracted_text'),
                original_image_path=final_image_path,
                photo_path=photo_path
            )
            
            db.add(student)
            db.commit()
            db.refresh(student)
            message = "Document uploaded and processed successfully"
        
        return UploadResponse(
            success=True,
            message=message,
            student=StudentResponse.from_orm(student),
            ocr_result=OCRResult(**ocr_result)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")


@app.get("/api/students", response_model=StudentSearchResponse)
async def search_students(
    query: Optional[str] = Query(None, description="Search by student ID or name"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Search and list students with pagination.
    Supports filtering by student ID or name.
    """
    try:
        # Base query
        base_query = db.query(Student)
        
        # Apply search filter
        if query:
            search_filter = f"%{query}%"
            base_query = base_query.filter(
                (Student.student_id.ilike(search_filter)) |
                (Student.full_name.ilike(search_filter))
            )
        
        # Get total count
        total = base_query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        students = base_query.order_by(Student.created_at.desc()).offset(offset).limit(page_size).all()
        
        return StudentSearchResponse(
            total=total,
            page=page,
            page_size=page_size,
            students=[StudentResponse.from_orm(s) for s in students]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching students: {str(e)}")


@app.get("/api/students/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Get a specific student by database ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentResponse.from_orm(student)


@app.put("/api/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Update student information."""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update fields
    update_data = student_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return StudentResponse.from_orm(student)


@app.delete("/api/students/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Delete a student record."""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete associated files
    try:
        if student.original_image_path and os.path.exists(student.original_image_path):
            os.remove(student.original_image_path)
        if student.photo_path and os.path.exists(student.photo_path):
            os.remove(student.photo_path)
    except Exception as e:
        print(f"Error deleting files: {str(e)}")
    
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted successfully"}


@app.get("/api/export/excel")
async def export_to_excel(
    query: Optional[str] = Query(None, description="Filter by student ID or name"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Export all students (or filtered) to Excel file.
    """
    try:
        # Base query
        base_query = db.query(Student)
        
        # Apply search filter if provided
        if query:
            search_filter = f"%{query}%"
            base_query = base_query.filter(
                (Student.student_id.ilike(search_filter)) |
                (Student.full_name.ilike(search_filter))
            )
        
        # Get all students
        students = base_query.order_by(Student.student_id).all()
        
        if not students:
            raise HTTPException(status_code=404, detail="No students found to export")
        
        # Generate Excel file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"students_export_{timestamp}.xlsx"
        output_path = os.path.join(settings.upload_dir, output_filename)
        
        ExcelService.export_students(students, output_path)
        
        # Return file
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting to Excel: {str(e)}")


@app.get("/api/files/{student_id}/{filename}")
async def get_file(student_id: str, filename: str):
    """Serve student files (images, photos)."""
    file_path = os.path.join(settings.upload_dir, student_id, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)


@app.get("/api/stats")
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Get system statistics."""
    try:
        total_students = db.query(Student).count()
        
        # Get students by department
        departments = db.query(
            Student.department,
            func.count(Student.id)
        ).group_by(Student.department).all()
        
        # Get recent uploads (last 7 days)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_uploads = db.query(Student).filter(
            Student.created_at >= week_ago
        ).count()
        
        return {
            "total_students": total_students,
            "recent_uploads": recent_uploads,
            "departments": [
                {"name": dept or "Unknown", "count": count}
                for dept, count in departments
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
