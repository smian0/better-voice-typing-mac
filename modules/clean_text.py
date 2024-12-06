def clean_transcription(text: str) -> str:
    """
    Basic text cleaning for transcription.
    """
    # Simple cleaning rules
    text = text.strip()
    # Ensure first character is capitalized
    if text and text[0].isalpha():
        text = text[0].upper() + text[1:]
    # Ensure there's a period at the end if the text ends with a letter or number
    if text and text[-1].isalnum():
        text += "."
    return text