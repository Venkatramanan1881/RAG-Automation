import mimetypes

def detect_file_types(uploaded_file: UploadFile) -> str:
    mime_type = uploaded_file.content_type

    if "audio" in mime_type:
        return "audio"
    elif "image" in mime_type:
        return "image"
    elif "pdf" in mime_type:
        return "pdf"
    elif "text" in mime_type:
        return "text"
    else:
        return "unknown"