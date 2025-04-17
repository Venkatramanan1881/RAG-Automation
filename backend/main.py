from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyBA0FSAKYF_OZWP6NhNDLzk4QaDCPCGZ9M")

app = FastAPI()

# Allow frontend dev server
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def chat_with_gemini(request: Request):
    data = await request.json()
    user_input = data.get("message")
    print(f"User input: {user_input}")

    if not user_input:
        return JSONResponse(status_code=400, content={"error": "Message is required"})

    try:
        # Send user input to Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )

        # 🧠 Extract the actual text reply from the response object
        gemini_reply = (
            response.candidates[0]
            .content.parts[0]
            .text.strip()
            if response.candidates and response.candidates[0].content.parts
            else "No reply from Gemini"
        )

        print(f"Gemini Reply: {gemini_reply}")
        return {"response": gemini_reply}

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"error": f"Internal Server Error: {str(e)}"})
