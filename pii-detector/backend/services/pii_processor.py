import re

def detect_pii(text):
    patterns = {
        "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b",
        "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Phone": r"\b\d{10}\b",
        "Email": r"\S+@\S+",
        "Credit Card": r"\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b"
    }

    result = {}

    for key, pattern in patterns.items():
        found = re.findall(pattern, text)
        if found:
            result[key] = found

    return result