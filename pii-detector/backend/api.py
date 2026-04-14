from flask import Blueprint, request, jsonify
from services.pii_processor import detect_pii
from services.redaction import redact_text

api = Blueprint('api', __name__)

@api.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    pii_data = detect_pii(text)
    return jsonify({'pii': pii_data}), 200

@api.route('/api/redact', methods=['POST'])
def redact():
    data = request.get_json()
    text = data.get('text', '')
    pii_data = data.get('pii', [])

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    redacted_text = redact_text(text, pii_data)
    return jsonify({'redacted_text': redacted_text}), 200