import requests
import json
import os

INPUT_FILE = "output.txt"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def parse_with_llm(input_path):
    """
    Reads raw text and uses Llama 3 (via Ollama) to extract structured JSON.
    """
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run extract_text.py first.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("Loading text into LLM context...")

    # Strict System Prompt to force JSON structure
    system_prompt = """
    You are an AI assistant that extracts structured data from documents.
    You MUST output ONLY valid JSON. No preamble, no markdown formatting, no explanations.
    
    Extract the following fields from the provided invoice text:
    - invoice_number (string or null)
    - date (string YYYY-MM-DD or null)
    - vendor_name (string or null)
    - total_amount (number or null)
    - items (list of objects with 'description' and 'amount')
    
    If a field is missing, use null.
    """

    prompt = f"DOCUMENT TEXT:\n{raw_text}\n\nJSON OUTPUT:"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "format": "json"  # Forces Ollama to output valid JSON
    }

    try:
        print(f"Sending request to Ollama ({MODEL_NAME})...")
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "")
        
        # Parse logic to ensure it's valid JSON
        structured_data = json.loads(generated_text)
        
        print("\n--- EXTRACTED JSON DATA ---\n")
        print(json.dumps(structured_data, indent=4))
        
        # Save to file
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=4)
        print("\nSaved to result.json")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        print("Make sure Ollama is running (ollama serve) and Llama 3 is pulled (ollama pull llama3).")
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        print("Raw Output:", generated_text)

if __name__ == "__main__":
    parse_with_llm(INPUT_FILE)
