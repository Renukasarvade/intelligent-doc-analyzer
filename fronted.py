import streamlit as st
import requests
import json
import threading
import subprocess
import time
from dotenv import load_dotenv
import os



# Start FastAPI backend
def start_backend():
    subprocess.Popen(["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"])
    time.sleep(3)

threading.Thread(target=start_backend, daemon=True).start()

# Streamlit UI
st.set_page_config(page_title="AI-Powered Document Analyzer", layout="wide")
st.title("📄 Intelligent Document Processing System")
st.write("Upload a document (PDF, DOCX, TXT) for automated analysis.")

BACKEND_URL = "http://localhost:8000"

# ========================
# UPLOAD SECTION
# ========================
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
text = ""

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    with st.spinner("Extracting text..."):
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        text = data["text"]
        st.success(f"✅ Text extracted from {uploaded_file.name}")
        st.text_area("Extracted Text", text, height=300)

        # ========================
        # SUMMARIZATION
        # ========================
        if st.button("Summarize Document"):
            with st.spinner("Summarizing..."):
                summary_response = requests.post(f"{BACKEND_URL}/analyze/summarize", data={"text": text})
            
            if summary_response.status_code == 200:
                st.subheader("📌 Summary")
                st.write(summary_response.json()["summary"])
            else:
                st.error("❌ Error summarizing document.")

        # ========================
        # ENTITY RECOGNITION
        # ========================
        if st.button("Extract Entities"):
            with st.spinner("Extracting entities..."):
                entities_response = requests.post(f"{BACKEND_URL}/analyze/entities", data={"text": text})
            
            if entities_response.status_code == 200:
                st.subheader("🧩 Extracted Entities")
                st.json(entities_response.json()["entities"])
            else:
                st.error("❌ Error extracting entities.")

        # ========================
        # KEY ELEMENTS
        # ========================
        if st.button("Extract Key Elements"):
            with st.spinner("Extracting key elements..."):
                key_elements_response = requests.post(f"{BACKEND_URL}/analyze/key_elements", data={"text": text})
            
            if key_elements_response.status_code == 200:
                st.subheader("🔑 Key Elements")
                st.write(key_elements_response.json()["key_elements"])
            else:
                st.error("❌ Error extracting key elements.")

        # ========================
        # Q&A
        # ========================
        question = st.text_input("Ask a question about the document:")
        if question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                qa_response = requests.post(f"{BACKEND_URL}/analyze/qa", data={"text": text, "question": question})
            
            if qa_response.status_code == 200:
                st.subheader("❓ Q&A Response")
                st.write(qa_response.json()["answer"])
            else:
                st.error("❌ Error in Q&A processing.")

        # ========================
        # DOCUMENT COMPARISON
        # ========================
        st.subheader("📑 Compare Two Documents")
        uploaded_file2 = st.file_uploader("Upload a second document", type=["pdf", "docx", "txt"], key="second_doc")
        
        if uploaded_file2:
            files2 = {"file": (uploaded_file2.name, uploaded_file2.getvalue(), uploaded_file2.type)}
            response2 = requests.post(f"{BACKEND_URL}/upload", files=files2)
            text2 = response2.json()["text"]
            
            if st.button("Compare Documents"):
                with st.spinner("Comparing..."):
                    compare_response = requests.post(f"{BACKEND_URL}/analyze/compare", data={"text1": text, "text2": text2})
                
                if compare_response.status_code == 200:
                    st.subheader("📊 Comparison Results")
                    st.write(compare_response.json()["comparison"])
                else:
                    st.error("❌ Error comparing documents.")
