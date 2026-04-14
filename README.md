# 🔐 PII Detection & Redaction Tool

A web-based application for detecting and redacting Personally Identifiable Information (PII) from documents and text.

## Features

- **Multiple File Formats**: Supports PDF, Images (PNG, JPG, JPEG, GIF, BMP), and plain text files
- **OCR Support**: Automatically extracts text from images using Tesseract
- **Advanced PII Detection**:
  - Aadhaar numbers
  - PAN (Permanent Account Number)
  - Phone numbers
  - Email addresses
  - Person names (using NLP)
- **Text Redaction**: Automatically redacts detected PII
- **Manual Input**: Paste or type text directly for analysis
- **Export Options**: Download redacted text as file or copy to clipboard
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites

- Python 3.8+
- Tesseract-OCR installed at `C:\Users\ASUS\Tesseract-OCR\tesseract.exe`

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd pii-detector
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

### Option 1: Flask Web Interface (Recommended)

```bash
python flask_app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Option 2: Streamlit Interface

```bash
streamlit run app.py
```

## Usage

### Web Interface (Flask)

1. **Upload & Scan Tab**:
   - Drag and drop a file or click to browse
   - Supported formats: PDF, Images (PNG, JPG, JPEG, GIF, BMP), TXT
   - Click "Scan for PII" to analyze

2. **Manual Input Tab**:
   - Paste or type text directly
   - Click "Analyze for PII" to detect sensitive information

3. **Results**:
   - View detected PII categorized by type
   - Preview extracted text
   - View redacted version with `[REDACTED]` placeholders
   - Download or copy redacted text

## Project Structure

```
pii-detector/
├── flask_app.py           # Flask backend application
├── app.py                 # Original Streamlit application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Styling
    └── script.js         # Client-side JavaScript
```

## Supported PII Types

| Type | Pattern |
|------|---------|
| Aadhaar | 1234 5678 9012 |
| PAN | ABCDE1234F |
| Phone | 9876543210 |
| Email | user@example.com |
| Names | Detected via NLP |

## Configuration

### Tesseract Path

If Tesseract is installed in a different location, update the path in `flask_app.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\path\to\tesseract.exe"
```

### File Size Limit

Default limit is 50MB. To change, modify in `flask_app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Change to desired size
```

## Security

- Files are processed locally and not stored permanently
- No data is sent to external servers for processing
- All detection happens on your machine

## Troubleshooting

**Issue**: "Tesseract is not installed or not found"
- **Solution**: Install Tesseract-OCR from https://github.com/UB-Mannheim/tesseract/wiki and update the path in `flask_app.py`

**Issue**: "spaCy model not found"
- **Solution**: Run `python -m spacy download en_core_web_sm`

**Issue**: PDF extraction returns empty text
- **Solution**: The PDF may be image-based. Use OCR on the PDF images directly or convert to images first.

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues or questions, please create an issue in the project repository.
