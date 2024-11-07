from openai import OpenAI

client = OpenAI()


# OpenAI Speech to text docs: https://platform.openai.com/docs/guides/speech-to-text
# ⚠️ IMPORTANT: OpenAI Audio API file uploads are currently limited to 25 MB



def transcribe_audio(filename):
    with open(filename, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text