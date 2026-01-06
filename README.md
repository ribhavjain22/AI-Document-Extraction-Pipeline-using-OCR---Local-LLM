# AI Document Extraction Pipeline (OCR + Local LLM)

## 📌 Project Overview
This project demonstrates a secure, local-only pipeline for extracting structured data from unstructured PDF documents (like invoices). It bridges the gap between traditional OCR and modern Generative AI.

**Workflow:**
1.  **Input**: PDF Document (e.g., Invoice)
2.  **OCR Layer**: `pytesseract` converts image-based PDFs into raw text.
3.  **Intelligence Layer**: `Ollama` (running Llama 3 locally) parses the raw text into structured JSON.
4.  **Output**: Clean JSON data ready for databases or APIs.

## 🚀 Why This Architecture?
-   **Privacy First**: No data leaves your machine. Perfect for sensitive financial/legal docs.
-   **Zero Cost**: No tokens, no API fees (unlike OpenAI/Azure).
-   **Latency**: Runs as fast as your hardware allows, no network overhead.

## 🛠️ Tech Stack
-   **Language**: Python 3.9+
-   **OCR Engine**: Tesseract OCR
-   **LLM Engine**: Ollama (hosting Llama 3)
-   **Libraries**: `pytesseract`, `pdf2image`, `requests`

---

## ⚙️ Setup Instructions

### 1. Prerequisites
-   **Python**: Installed [Download Here](https://www.python.org/)
-   **Tesseract OCR**:
    -   *Windows*: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Add to PATH during install).
-   **Poppler** (for PDF conversion):
    -   *Windows*: [Download Binary](https://github.com/oschwartz10612/poppler-windows/releases/), extract, and add `bin` folder to your System PATH.
-   **Ollama**:
    -   Download from [ollama.com](https://ollama.com/)
    -   Run `ollama run llama3` in your terminal to pull the model.

### 2. Installation
Clone the project and navigate to the directory:
```bash
cd ai-document-extraction-demo
```

Create and activate the virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Usage
**Step 1: Place your PDF**
Put your target PDF (e.g., `invoice.pdf`) inside the `input_docs/` folder.
*Rename it to `sample_invoice.pdf` or update the path in `extract_text.py`.*

**Step 2: Run OCR Extraction**
```bash
python extract_text.py
```
*Creates `output.txt` containing the raw string data.*

**Step 3: Run LLM Structuring**
Ensure Ollama is running (`ollama serve`) and llama3 model pulled(ollama pull llama3).
```bash
python llm_parser.py
```
*Reads `output.txt`, queries Llama 3, and saves `result.json`.*

### ✅ Example Output (result.json)
```json
{
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "vendor_name": "Tech Solutions Inc.",
    "total_amount": 1500.00,
    "items": [
        {
            "description": "Dell XPS 15 Laptop",
            "amount": 1200.00
        },
        {
            "description": "Logitech MX Master 3",
            "amount": 100.00
        }
    ]
}
```

---

## 💬 Interview Talking Points
If asked about this project in an AI Engineer interview:

1.  **"Why not just use GPT-4?"**
    *   *"I chose a local setup to demonstrate data privacy compliance (GDPR/HIPAA). Sending financial docs to an external API is often a security risk for enterprise clients."*

2.  **"How do you handle OCR errors?"**
    *   *"Tesseract is good but not perfect. Using Llama 3 acts as a correction layer—it can infer context even if a character is slightly misread (e.g., '1nvoice' -> 'Invoice')."*

3.  **"How is the JSON structure guaranteed?"**
    *   *"I used Ollama's `format: 'json'` parameter combined with a strict system prompt. This constrains the LLM's decoding strategy to only generate valid JSON tokens."*
