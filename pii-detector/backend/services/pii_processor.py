def detect_pii(text):
    import re

    # Define regex patterns for different types of PII
    patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\+?\d[\d -]{8,12}\d',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b(?:\d{4}[- ]?){3}\d{4}\b',
        'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'  # Simple name pattern
    }

    detected_pii = {}

    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            detected_pii[pii_type] = matches

    return detected_pii