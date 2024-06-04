from PIL import Image
import base64
from typing import Iterator
from cat.log import log
from langchain.schema import Document
from langchain.document_loaders.blob_loaders import Blob
from langchain.document_loaders.base import BaseBlobParser
from io import BytesIO
from PIL import Image
from .ocr_processor import OCRProcessor

class ImageParser(BaseBlobParser):
    """Parser for image blobs."""

    def __init__(self):
        pass

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        binary_data = blob.as_bytes()

        if len(binary_data) > 20 * 1000000:
            content = "The image is too large to be processed."
        else:
            try:
                image = Image.open(BytesIO(binary_data))
                model = OCRProcessor()

                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                content = model.process_image(image)

            except Exception as e:
                log.error(f"Error processing image: {e}")
                content = "Error processing image."

        yield Document(
            page_content=content,
            metadata={
                "source": "Cat_Latex",
                "name": blob.path.rsplit('.', 1)[0],
                "image_type": "image/png"
            }
        )