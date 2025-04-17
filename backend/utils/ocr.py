from google import genai
import os

async def extract_text_from_image_or_pdf(file):
    """
    Extract text from image or PDF files using Google Gemini.
    """
    # Initialize the Gemini client
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

    # Read the file
    with open(file, "rb") as file_data:
        file_content = file_data.read()

    # Send the file data to Gemini for OCR
    response = client.models.extract_text(
        model="gemini-2.0-flash",
        contents=file_content,
        mime_type="application/pdf" if file.endswith('.pdf') else "image/jpeg"
    )

    # Extract the text from the response
    extracted_text = (
        response.candidates[0]
        .content.parts[0]
        .text.strip()
        if response.candidates and response.candidates[0].content.parts
        else "No text extracted"
    )

    return extracted_text