def redact_text(text, pii_data):
    """
    Redacts detected PII from the given text.

    Parameters:
    - text (str): The original text containing PII.
    - pii_data (list): A list of detected PII strings to be redacted.

    Returns:
    - str: The text with PII redacted.
    """
    for pii in pii_data:
        text = text.replace(pii, "[REDACTED]")
    return text