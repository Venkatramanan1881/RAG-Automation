from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
import os
from dotenv import load_dotenv
import drive_upload

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

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

    if not user_input:
        return JSONResponse(status_code=400, content={"error": "Message is required"})

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )
        gemini_reply = (
            response.candidates[0].content.parts[0].text.strip()
            if response.candidates and response.candidates[0].content.parts
            else "No reply from Gemini"
        )
        return {"response": gemini_reply}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal Server Error: {str(e)}"})


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    upload_dir: str = Form(...)
):
    try:
        os.makedirs(upload_dir, exist_ok=True)
        filename = file.filename
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Folder mapping based on extension
        folder_map = {
            ".pdf": "1t6L_RwykbMY7fIBCcjSGws0i_b3B2YFy",
            ".jpg": "1ZZ1Vs2Gc6pZFzQse7coY8KB4zNU5KgHU",
            ".jpeg": "1ZZ1Vs2Gc6pZFzQse7coY8KB4zNU5KgHU",
            ".png": "1ZZ1Vs2Gc6pZFzQse7coY8KB4zNU5KgHU",
            ".gif": "1ZZ1Vs2Gc6pZFzQse7coY8KB4zNU5KgHU"
        }

        try:
            success = drive_upload.upload_to_drive(filename, file_path, folder_map)

            if success:
                drive_upload.delete_local_file(file_path)
                return {"filename": filename, "message": "Uploaded to Drive and deleted locally"}
            else:
                return JSONResponse(status_code=500, content={"error": "Failed to upload to Drive"})
        except Exception as e:
            print(f"Drive upload error: {str(e)}")
            return JSONResponse(status_code=500, content={"error": f"Drive upload error: {str(e)}"})

    except OSError as e:
        print(f"File system error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"File system error: {str(e)}"})
    except Exception as e:
        print(f"Internal Server Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"Internal Server Error: {str(e)}"})
