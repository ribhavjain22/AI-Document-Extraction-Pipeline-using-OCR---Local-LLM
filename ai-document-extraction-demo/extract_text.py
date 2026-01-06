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

def extract_text_from_pdf(pdf_path, output_path):
    """
    Converts a PDF to images and uses Tesseract OCR to extract text.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        print("Please place a 'sample_invoice.pdf' in the 'input_docs' folder.")
        return

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
            print(f"Using local Poppler at: {local_poppler_bin}")
            poppler_path = local_poppler_bin

        # Convert PDF to list of images (one per page)
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        print("Ensure 'poppler' is installed and added to PATH.")
        return

    extracted_text = ""
    
    for i, image in enumerate(images):
        print(f"OCR processing page {i + 1}...")
        text = pytesseract.image_to_string(image)
        extracted_text += f"--- Page {i + 1} ---\n{text}\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    print(f"Extraction complete! Text saved to {output_path}")

if __name__ == "__main__":
    extract_text_from_pdf(PDF_PATH, OUTPUT_FILE)
