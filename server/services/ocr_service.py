import pytesseract
import cv2
import numpy as np
from PIL import Image
import re
import os
from typing import Optional, Tuple, Dict
from config import get_settings

settings = get_settings()

# Set tesseract command path
if settings.tesseract_cmd and os.path.exists(settings.tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


class OCRService:
    """Service for OCR text extraction from documents."""
    
    @staticmethod
    def preprocess_image(image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR results.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to make text more clear
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Apply slight dilation to make text thicker
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.dilate(denoised, kernel, iterations=1)
        
        return processed
    
    @staticmethod
    def extract_text(image_path: str) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text
        """
        try:
            # Preprocess image
            processed_img = OCRService.preprocess_image(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_img, lang='eng')
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""
    
    @staticmethod
    def extract_student_data(text: str) -> Dict[str, Optional[str]]:
        """
        Extract structured student data from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Dictionary with extracted student information
        """
        data = {
            'student_id': None,
            'full_name': None,
            'email': None,
            'phone': None,
            'department': None,
            'program': None,
            'year_of_study': None,
        }
        
        # Normalize text
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Extract Student ID (various formats)
        student_id_patterns = [
            r'(?:Student\s*ID|ID\s*No|ID\s*Number|Matric\s*No)[:\s]*([A-Z0-9\-/]+)',
            r'\b([A-Z]{2,}\d{4,})\b',  # Format like CS20221234
            r'\b(\d{6,10})\b',  # Pure numeric IDs
        ]
        
        for pattern in student_id_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['student_id'] = match.group(1).strip()
                break
        
        # Extract Name
        name_patterns = [
            r'(?:Name|Student\s*Name|Full\s*Name)[:\s]*([A-Za-z\s]{3,50}?)(?:\s*(?:ID|Student|Department|DOB|Date)|\s*\d|\s*$)',
            r'(?:^|\n)([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})(?:\s|$)',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 5:  # Reasonable name length
                    data['full_name'] = name
                    break
        
        # Extract Email
        email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            data['email'] = email_match.group(1)
        
        # Extract Phone
        phone_patterns = [
            r'(?:Phone|Tel|Mobile|Contact)[:\s]*([+\d\s\-()]{10,20})',
            r'\b(\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4})\b',
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['phone'] = match.group(1).strip()
                break
        
        # Extract Department
        dept_pattern = r'(?:Department|Dept|Faculty)[:\s]*([A-Za-z\s&]{3,50}?)(?:\s*(?:Program|Course|Year|Student)|\s*$)'
        dept_match = re.search(dept_pattern, text, re.IGNORECASE)
        if dept_match:
            data['department'] = dept_match.group(1).strip()
        
        # Extract Program
        program_pattern = r'(?:Program|Course|Major)[:\s]*([A-Za-z\s&]{3,50}?)(?:\s*(?:Year|Level|Student)|\s*$)'
        program_match = re.search(program_pattern, text, re.IGNORECASE)
        if program_match:
            data['program'] = program_match.group(1).strip()
        
        # Extract Year of Study
        year_patterns = [
            r'(?:Year|Level|Class)[:\s]*(\d{1,2}|First|Second|Third|Fourth|Final)',
            r'\b(Year\s*\d|Level\s*\d)\b',
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['year_of_study'] = match.group(1).strip()
                break
        
        return data
    
    @staticmethod
    def detect_and_extract_photo(image_path: str, output_dir: str) -> Optional[str]:
        """
        Detect and extract student photo from document.
        
        Args:
            image_path: Path to the document image
            output_dir: Directory to save extracted photo
            
        Returns:
            Path to extracted photo or None
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50)
            )
            
            if len(faces) > 0:
                # Get the largest face (likely the student photo)
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = largest_face
                
                # Add some padding
                padding = 10
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(img.shape[1] - x, w + 2 * padding)
                h = min(img.shape[0] - y, h + 2 * padding)
                
                # Extract face
                face_img = img[y:y+h, x:x+w]
                
                # Save extracted photo
                os.makedirs(output_dir, exist_ok=True)
                photo_filename = f"photo_{os.path.basename(image_path)}"
                photo_path = os.path.join(output_dir, photo_filename)
                cv2.imwrite(photo_path, face_img)
                
                return photo_path
            
            return None
            
        except Exception as e:
            print(f"Error extracting photo: {str(e)}")
            return None
    
    @staticmethod
    def process_document(image_path: str, output_dir: str) -> Dict:
        """
        Complete document processing: OCR + photo extraction.
        
        Args:
            image_path: Path to the document image
            output_dir: Directory for saving processed files
            
        Returns:
            Dictionary with processing results
        """
        result = {
            'success': False,
            'extracted_text': None,
            'student_data': None,
            'photo_path': None,
            'photo_extracted': False,
            'error': None
        }
        
        try:
            # Extract text
            text = OCRService.extract_text(image_path)
            result['extracted_text'] = text
            
            # Extract structured data
            if text:
                student_data = OCRService.extract_student_data(text)
                result['student_data'] = student_data
            
            # Extract photo
            photo_path = OCRService.detect_and_extract_photo(image_path, output_dir)
            if photo_path:
                result['photo_path'] = photo_path
                result['photo_extracted'] = True
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
