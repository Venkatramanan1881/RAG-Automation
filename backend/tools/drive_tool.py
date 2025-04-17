from pydantic import BaseModel
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import os

# === Predefined Folder IDs ===
FOLDER_IDS = {
    "RAG": "1t6L_RwykbMY7fIBCcjSGws0i_b3B2YFy",
    "Invoice": "1ZZ1Vs2Gc6pZFzQse7coY8KB4zNU5KgHU",
    "Visiting Card": "1AHTQs-_XlQIOQYFmwiuvzJBLZvS45MOC"
}

# === Input Schema ===
class UploadFileInput(BaseModel):
    file_path: str  # Local path to the PDF
    folder_type: str  # One of: RAG, Invoice, Visiting Card

# === Core Upload Function ===
def upload_file_to_drive(input: UploadFileInput) -> str:
    folder_id = FOLDER_IDS.get(input.folder_type)
    if not folder_id:
        return f"❌ Invalid folder type: {input.folder_type}. Must be one of: {list(FOLDER_IDS.keys())}"
    if not input.file_path.endswith(".pdf"):
        return "❌ Only PDF files are supported."

    creds = pickle.load(open("token.pickle", "rb"))
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        'name': os.path.basename(input.file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(input.file_path, mimetype='application/pdf')
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()

    return f"✅ Uploaded: {file.get('name')} ➜ Folder: {input.folder_type}"

# === Tool Registration ===
drive_tool = {
    "name": "upload_pdf_to_drive",
    "description": "Uploads a PDF to the RAG, Invoice, or Visiting Card folder in Google Drive.",
    "parameters": UploadFileInput.schema(),
    "function": upload_file_to_drive
}
