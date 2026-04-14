import streamlit as st
import re
import spacy
import pytesseract
from PIL import Image
import pdfplumber
import io

# ---------------------------
# SET TESSERACT PATH (IMPORTANT)
# ---------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\Tesseract-OCR\tesseract.exe"

# ---------------------------
# LOAD NLP MODEL
# ---------------------------
nlp = spacy.load("en_core_web_sm")

# ---------------------------
# PII PATTERNS
# ---------------------------
patterns = {
    "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "Phone": r"\b\d{10}\b",
    "Email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
}

# ---------------------------
# TEXT EXTRACTION FUNCTION
# ---------------------------
def extract_text(uploaded_file, file_type):
    if file_type == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_type == "image":
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)

    elif file_type == "text":
        return uploaded_file.read().decode("utf-8")

# ---------------------------
# PII DETECTION FUNCTION
# ---------------------------
def detect_pii(text):
    results = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[key] = matches

    # NLP for names
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if names:
        results["Names"] = names

    return results

# ---------------------------
# REDACTION FUNCTION
# ---------------------------
def redact_text(text):
    redacted = text

    for pattern in patterns.values():
        redacted = re.sub(pattern, "XXXXXX", redacted)

    return redacted

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="PII Detector", layout="centered")

st.title("🔐 PII Detection & Redaction Tool")

st.write("Upload a file (PDF, Image, or Text) to detect sensitive information.")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "png", "jpg", "jpeg", "txt"])

if uploaded_file:
    file_type = ""

    if uploaded_file.name.endswith(".pdf"):
        file_type = "pdf"
    elif uploaded_file.name.endswith((".png", ".jpg", ".jpeg")):
        file_type = "image"
    elif uploaded_file.name.endswith(".txt"):
        file_type = "text"

    if st.button("Scan for PII"):
        text = extract_text(uploaded_file, file_type)

        st.subheader("📄 Extracted Text")
        st.write(text[:1000])

        pii = detect_pii(text)

        st.subheader("🔍 Detected PII")
        if pii:
            st.json(pii)
        else:
            st.success("No PII found!")

        redacted = redact_text(text)

        st.subheader("🧹 Redacted Text")
        st.write(redacted[:1000])