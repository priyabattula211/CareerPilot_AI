import fitz  # PyMuPDF
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_text_from_pdf(pdf_bytes):
    """Extracts raw text from a PDF file."""
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
    return text
