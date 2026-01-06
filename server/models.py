from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary, Index
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class Student(Base):
    """Student model for storing student information extracted from documents."""
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    email = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(200), nullable=True)
    program = Column(String(200), nullable=True)
    year_of_study = Column(String(50), nullable=True)
    
    # Document information
    document_type = Column(String(100), nullable=True)
    extracted_text = Column(Text, nullable=True)
    
    # File paths
    original_image_path = Column(String(500), nullable=True)
    photo_path = Column(String(500), nullable=True)
    processed_image_path = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional indexes for efficient searching
    __table_args__ = (
        Index('idx_student_search', 'student_id', 'full_name'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Student(id={self.id}, student_id='{self.student_id}', name='{self.full_name}')>"
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'program': self.program,
            'year_of_study': self.year_of_study,
            'document_type': self.document_type,
            'extracted_text': self.extracted_text,
            'original_image_path': self.original_image_path,
            'photo_path': self.photo_path,
            'processed_image_path': self.processed_image_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
