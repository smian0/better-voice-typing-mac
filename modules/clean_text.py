from .completion import get_anthropic_completion

def clean_transcription(text):
    """
    Cleans and corrects voice-to-text transcription using Anthropic's Claude model.
    """
    prompt = """
Your task is to correct the following voice-to-text transcript, if necessary, while preserving the original meaning:
<text>
{}
</text>
Respond only with the corrected text, nothing else.
    """.strip().format(text)

    cleaned_text = get_anthropic_completion(
        messages=[{"role": "user", "content": prompt}],
        model="claude-3-haiku-20240307",
        temperature=0.3
    )

    return cleaned_text