from cat.log import log
from PIL import Image
from pix2tex.cli import LatexOCR

class OCRProcessor:
    """Class to process images using OCR."""
    
    def __init__(self):
        self.model = LatexOCR()
    
    def process_image(self, image: Image) -> str:
        """Process the image to extract text using OCR."""
        try:
            return self.model(image)
        except Exception as e:
            log.error(f"OCR processing failed: {e}")
            raise