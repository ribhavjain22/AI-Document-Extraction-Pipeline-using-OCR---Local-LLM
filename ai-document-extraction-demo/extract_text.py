import pytesseract
from pdf2image import convert_from_path
import os
import sys

# Configuration
# If Tesseract is not in your PATH, uncomment and set the path below:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Auto-detect default Windows installation
default_tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(default_tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = default_tesseract_path

PDF_PATH = os.path.join("input_docs", "sample_invoice.pdf")
OUTPUT_FILE = "output.txt"

def extract_text_from_pdf(pdf_path):
    """
    Converts a PDF to images and uses Tesseract OCR to extract text.
    Returns: Extracted text as a string.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return None

    print(f"Processing {pdf_path}...")
    
    try:
        # Check for local poppler installation
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_poppler_bin = os.path.join(script_dir, "poppler", "Library", "bin")
        if not os.path.exists(local_poppler_bin):
            # Fallback for different folder structure
            local_poppler_bin = os.path.join(script_dir, "poppler", "bin")
        
        poppler_path = None
        if os.path.exists(local_poppler_bin):
            # print(f"Using local Poppler at: {local_poppler_bin}")
            poppler_path = local_poppler_bin

        # Convert PDF to list of images (one per page)
        # Increasing DPI to 300 helps Tesseract keep columns aligned
        images = convert_from_path(pdf_path, poppler_path=poppler_path, dpi=300)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return None

    extracted_text = ""
    
    for i, image in enumerate(images):
        # text = pytesseract.image_to_string(image)
        # extracted_text += f"--- Page {i + 1} ---\n{text}\n"
        # Optimize for speed/accuracy?
        text = pytesseract.image_to_string(image)
        extracted_text += f"--- Page {i + 1} ---\n{text}\n"

    return extracted_text

if __name__ == "__main__":
    text = extract_text_from_pdf(PDF_PATH)
    if text:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extraction complete! Text saved to {OUTPUT_FILE}")
