from google import genai
import os

async def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio files using Google Gemini.
    """
    # Initialize the Gemini client
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

    # Read the audio file
    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Send the audio data to Gemini for transcription
    response = client.models.transcribe(
        model="gemini-2.0-flash",
        contents=audio_data,
        mime_type="audio/wav"
    )

    # Extract the transcription from the response
    transcription = (
        response.candidates[0]
        .content.parts[0]
        .text.strip()
        if response.candidates and response.candidates[0].content.parts
        else "No transcription available"
    )

    return transcription