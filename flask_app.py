from flask import Flask, render_template, request, jsonify
import re
try:
    import spacy
except ImportError:
    spacy = None
import pytesseract
from PIL import Image
import pdfplumber
import io
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# ---------------------------
# SET TESSERACT PATH
# ---------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\Tesseract-OCR\tesseract.exe"

# ---------------------------
# LOAD NLP MODEL
# ---------------------------
nlp = None
if spacy:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Warning: spaCy model not found. Name detection will be disabled.")

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
def extract_text(file_content, file_type, filename):
    try:
        if file_type == "pdf":
            file_obj = io.BytesIO(file_content)
            with pdfplumber.open(file_obj) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text

        elif file_type == "image":
            file_obj = io.BytesIO(file_content)
            image = Image.open(file_obj)
            return pytesseract.image_to_string(image)

        elif file_type == "text":
            return file_content.decode("utf-8")
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

# ---------------------------
# PII DETECTION FUNCTION
# ---------------------------
def detect_pii(text):
    results = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[key] = list(set(matches))  # Remove duplicates

    # NLP for names (only if spaCy model is available)
    if nlp:
        try:
            doc = nlp(text)
            names = list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"]))
            if names:
                results["Names"] = names
        except Exception as e:
            print(f"NLP error: {str(e)}")

    return results

# ---------------------------
# REDACTION FUNCTION
# ---------------------------
def redact_text(text):
    redacted = text

    for pattern in patterns.values():
        redacted = re.sub(pattern, "[REDACTED]", redacted)

    return redacted

# ---------------------------
# ROUTES
# ---------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        filename = file.filename
        file_content = file.read()
        
        # Determine file type
        if filename.endswith('.pdf'):
            file_type = 'pdf'
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_type = 'image'
        elif filename.endswith('.txt'):
            file_type = 'text'
        else:
            return jsonify({"error": "Unsupported file type. Use PDF, Image, or TXT."}), 400

        # Extract text
        text = extract_text(file_content, file_type, filename)
        
        if not text or not text.strip():
            return jsonify({"error": "No text found in file"}), 400

        # Detect PII
        pii = detect_pii(text)

        # Create redacted version
        redacted = redact_text(text)

        return jsonify({
            "status": "success",
            "filename": filename,
            "extracted_text": text[:2000],  # First 2000 chars
            "full_text": text,
            "pii_detected": pii,
            "redacted_text": redacted,
            "has_pii": len(pii) > 0,
            "pii_count": sum(len(v) for v in pii.values())
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/redact', methods=['POST'])
def redact():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        redacted = redact_text(text)
        pii = detect_pii(text)

        return jsonify({
            "status": "success",
            "original_text": text,
            "redacted_text": redacted,
            "pii_found": pii,
            "has_pii": len(pii) > 0
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
