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
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"Uploaded {len(uploaded_files)} files. Ready to process.")
    
    if st.button("Process Batch"):
        results = []
        progress_bar = st.progress(0)
        
        # Create tabs for detailed view
        tabs = st.tabs([f.name for f in uploaded_files])
        
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)

        for i, uploaded_file in enumerate(uploaded_files):
            # Save file temporarily
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with tabs[i]:
                st.subheader(f"Processing: {uploaded_file.name}")
                
                # 1. OCR
                with st.spinner("Step 1: OCR Extraction..."):
                    raw_text = extract_text_from_pdf(temp_path)
                
                if raw_text:
                    with st.expander("View Raw OCR Text"):
                        st.text_area("Content", raw_text, height=150)
                        
                    # 2. LLM
                    with st.spinner("Step 2: AI Analysis..."):
                        structured_data = parse_with_llm(raw_text, doc_type.lower())
                    
                    st.json(structured_data)
                    results.append({
                        "filename": uploaded_file.name,
                        "data": structured_data
                    })
                else:
                    st.error("OCR Failed.")
                    results.append({"filename": uploaded_file.name, "error": "OCR Failed"})
            
            # Update progress
            progress_bar.progress((i + 1) / len(uploaded_files))

        st.success("Batch Processing Complete!")
        
        # Summary Section
        st.divider()
        st.header("Batch Summary")
        
        # Create a downloadable merged JSON
        merged_json = json.dumps(results, indent=4)
        st.download_button(
            label="Download All Results (JSON)",
            data=merged_json,
            file_name="batch_results.json",
            mime="application/json"
        )
