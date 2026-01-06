import requests
import json
import os

INPUT_FILE = "output.txt"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def parse_with_llm(raw_text, doc_type="invoice"):
    """
    Uses Llama 3 to extract structured JSON from raw text.
    """
    
    # Select prompt based on document type
    if doc_type == "resume":
        system_prompt = """
        You are an AI assistant that extracts structured data from resumes.
        You MUST output ONLY valid JSON.
        Extract:
        - full_name (string)
        - email (string)
        - phone (string)
        - skills (list of strings)
        - experience (list of objects with company, role, duration)
        - education (list of objects with institution, degree)
        """
    else: # Default to Invoice
        system_prompt = """
        You are an AI assistant that extracts structured data from invoices.
        The document may contain multiple pages. You MUST extract all line items from EVERY page.
        
        You MUST output ONLY valid JSON using the exact schema below.
        
        REQUIRED SCHEMA:
        {
          "invoice_metadata": {
            "invoice_number": "string",
            "invoice_date": "YYYY-MM-DD",
            "currency": "string (e.g. EUR, USD)"
          },
          "seller": {
            "company_name": "string",
            "address": "string",
            "phone": "string"
          },
          "buyer": {
            "name": "string",
            "address": "string",
            "phone": "string"
          },
          "line_items": [
            {
              "description": "string",
              "quantity": number,
              "unit_price": number,
              "line_total": number
            }
          ],
          "totals": {
            "subtotal": number,
            "tax": number,
            "shipping": number,
            "total_due": number
          }
        }
        
        If a field is missing, use null. ensure numeric values are numbers, not strings.
        """

    prompt = f"DOCUMENT TEXT:\n{raw_text}\n\nJSON OUTPUT:"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "format": "json"
    }

    try:
        # print(f"Sending request to Ollama ({MODEL_NAME})...")
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "")
        
        structured_data = json.loads(generated_text)
        return structured_data

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        return {"error": "Invalid JSON response from LLM", "raw_output": generated_text}

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        
        data = parse_with_llm(text, "invoice")
        print(json.dumps(data, indent=4))
        
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
