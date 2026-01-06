# Make OCR service optional
try:
    from .ocr_service import OCRService
    __all__ = ['OCRService', 'ExcelService']
except ImportError:
    __all__ = ['ExcelService']

from .excel_service import ExcelService
