from openai import OpenAI

client = OpenAI()  # This will use OPENAI_API_KEY from environment by default

def transcribe_audio(filename):
    with open(filename, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text 