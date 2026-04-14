import re

def detect_pii(text):
    patterns = {
        "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b",
        "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Phone": r"\b\d{10}\b",
        "Email": r"\S+@\S+",
    }

    results = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[key] = matches

    return results