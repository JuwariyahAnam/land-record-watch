"""VerbX client. Open the VerbX docs, copy the text-to-speech example and paste it here.
Keep the key in the environment. Every demo alert must come from a real VerbX call."""
import os


def speak(text, language):
    """Return audio bytes (MP3 or WAV) for text in the language ('kn', 'hi', 'en').
    TODO: endpoint, auth header, request body, language and voice codes, from the docs."""
    key = os.environ["VERBX_API_KEY"]  # noqa: F841
    raise NotImplementedError("fill in from the VerbX docs")


def transcribe(audio_bytes, language):
    """Optional: speech to text for voice questions. Same rule, from the docs."""
    raise NotImplementedError("fill in from the VerbX docs")
