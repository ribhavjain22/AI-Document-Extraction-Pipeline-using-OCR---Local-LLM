import streamlit as st
import os
import time
import json
from extract_text import extract_text_from_pdf
from llm_parser import parse_with_llm

st.set_page_config(page_title="AI Doc Extractor", layout="wide")

st.title("📄 AI Document Extraction Pipeline")
st.markdown("Extract structured data from **Invoices** or **Resumes** using Local OCR and Llama 3.")

# Sidebar configuration
with st.sidebar:
    st.header("Upload Configuration")
    doc_type = st.selectbox("Select Document Type", ["Invoice", "Resume"])
    st.info(f"Mode: Extracting {doc_type} data")

# File Uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Save file temporarily to disk because pdf2image needs a file path
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. OCR Extraction (Tesseract)")
        with st.spinner("Extracting text from PDF..."):
            raw_text = extract_text_from_pdf(temp_path)
            
        if raw_text:
            with st.expander("View Raw Extracted Text", expanded=False):
                st.text_area("Raw Text", raw_text, height=300)
        else:
            st.error("OCR failed to extract text.")
            st.stop()

    with col2:
        st.subheader("2. AI Analysis (Llama 3)")
        if st.button("Extract Data with Llama 3"):
            with st.spinner("Analyzing text with Llama 3..."):
                start_time = time.time()
                structured_data = parse_with_llm(raw_text, doc_type.lower())
                end_time = time.time()
                
            st.success(f"Analysis Complete in {end_time - start_time:.2f}s")
            
            st.subheader("Structured Output")
            st.json(structured_data)
            
            # Download button
            json_str = json.dumps(structured_data, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{doc_type.lower()}_data.json",
                mime="application/json"
            )

    # Cleanup temp file (optional, depends on use case)
    # os.remove(temp_path)
