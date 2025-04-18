import os
from drive_auth import get_drive_service
from googleapiclient.http import MediaFileUpload


def upload_to_drive(filename, filepath, folder_map):
    try:
        service = get_drive_service()

        ext = os.path.splitext(filename)[1].lower()
        folder_id = folder_map.get(ext)
        if not folder_id:
            print(f"[Drive Upload Error] No folder ID mapped for extension: {{ext}}")
            return False

        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaFileUpload(filepath, mimetype='*/*', resumable=True)
        uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"[Drive Upload] File uploaded. ID: {uploaded.get('id')}")
        return True

    except Exception as e:
        print(f"[Drive Upload Error] {str(e)}")
        return False


def upload_file_to_drive(file_path, file_name, folder_id=None):
    service = get_drive_service()

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')



def delete_local_file(filepath):
    try:
        os.remove(filepath)
        print(f"[File Delete] Deleted {filepath}")
    except Exception as e:
        print(f"[File Delete Error] {str(e)}")
