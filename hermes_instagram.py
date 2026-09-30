import io
import json
import os
import tempfile
import time
from pathlib import Path

import requests
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

DRIVE_VIDEOS_FOLDER_ID = os.getenv("DRIVE_VIDEOS_FOLDER_ID", "14PBXxE_6fQrPHCvuZGYiZrecpWJ0759R")
DRIVE_PROJECT_FOLDER_ID = os.getenv("DRIVE_PROJECT_FOLDER_ID", "1SXaqtqMVNh8kfN200GNzEpgA3kid486m")
STATE_FILE_NAME = ".hermes_instagram_state.json"

IG_USER_ID = os.getenv("IG_USER_ID", "")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN", "")
GRAPH_VERSION = os.getenv("GRAPH_VERSION", "v24.0")
CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", "{name}\n\n#reels #video #instagram")


def drive_service():
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    token_file = os.getenv("GOOGLE_OAUTH_TOKEN_FILE")

    if service_account_file:
        creds = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/drive"],
        )
    elif token_file:
        creds = Credentials.from_authorized_user_file(
            token_file,
            scopes=["https://www.googleapis.com/auth/drive"],
        )
    else:
        raise RuntimeError(
            "Google Drive kimliği yok. GOOGLE_SERVICE_ACCOUNT_FILE veya "
            "GOOGLE_OAUTH_TOKEN_FILE ayarlanmalı."
        )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def list_videos(drive):
    q = (
        f"'{DRIVE_VIDEOS_FOLDER_ID}' in parents and trashed=false "
        "and mimeType contains 'video/'"
    )
    files = []
    page_token = None
    while True:
        res = drive.files().list(
            q=q,
            fields="nextPageToken,files(id,name,mimeType,createdTime,modifiedTime,size)",
            orderBy="createdTime asc,name",
            pageSize=1000,
            pageToken=page_token,
        ).execute()
        files.extend(res.get("files", []))
        page_token = res.get("nextPageToken")
        if not page_token:
            return files


def _find_state_file(drive):
    q = (
        f"'{DRIVE_PROJECT_FOLDER_ID}' in parents and trashed=false "
        f"and name='{STATE_FILE_NAME}'"
    )
    res = drive.files().list(q=q, fields="files(id,name)", pageSize=10).execute()
    return res.get("files", [])


def load_state(drive):
    found = _find_state_file(drive)
    if not found:
        return {"published_drive_file_ids": {}, "version": 1}

    data = drive.files().get_media(fileId=found[0]["id"]).execute()
    try:
        return json.loads(data.decode("utf-8"))
    except Exception:
        return {"published_drive_file_ids": {}, "version": 1}


def save_state(drive, state):
    payload = json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8")
    found = _find_state_file(drive)

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(payload)
        tmp_path = tmp.name

    try:
        media = MediaFileUpload(tmp_path, mimetype="application/json", resumable=False)
        if found:
            drive.files().update(fileId=found[0]["id"], media_body=media).execute()
        else:
            drive.files().create(
                body={"name": STATE_FILE_NAME, "parents": [DRIVE_PROJECT_FOLDER_ID]},
                media_body=media,
                fields="id",
            ).execute()
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def download_video(drive, file_id, name):
    suffix = Path(name).suffix or ".mp4"
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)

    request = drive.files().get_media(fileId=file_id)
    with open(path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return path


def instagram_create_reel_from_local_file(video_path, caption):
    """
    Meta/Instagram upload adımı burada izole edilmiştir.
    API kimlikleri hazırlandıktan sonra bu fonksiyon Meta'nın güncel
    Instagram Reels yayınlama akışına göre etkinleştirilecektir.
    """
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        raise RuntimeError("IG_USER_ID ve IG_ACCESS_TOKEN henüz ayarlanmadı.")

    raise RuntimeError(
        "Instagram API bağlantısı henüz etkinleştirilmedi. "
        "Drive tarama ve tekrar-yüklemeyi önleme sistemi hazır."
    )


def run_once():
    drive = drive_service()
    state = load_state(drive)
    published = state.setdefault("published_drive_file_ids", {})

    videos = list_videos(drive)
    new_videos = [v for v in videos if v["id"] not in published]

    print(f"Drive'da {len(videos)} video bulundu; yeni: {len(new_videos)}")
    if not new_videos:
        print("Yeni video yok. İşlem yapılmadı.")
        return

    for video in new_videos:
        print(f"Yeni video: {video['name']} ({video['id']})")
        local_path = download_video(drive, video["id"], video["name"])
        try:
            caption = CAPTION_TEMPLATE.format(
                name=Path(video["name"]).stem,
                filename=video["name"],
            )
            result = instagram_create_reel_from_local_file(local_path, caption)

            # Yalnızca Instagram gerçekten başarılı olursa işlendi olarak kaydet.
            published[video["id"]] = {
                "name": video["name"],
                "instagram_result": result,
                "published_at_unix": int(time.time()),
            }
            save_state(drive, state)
            print("Yayınlandı ve durum kaydedildi.")
        finally:
            Path(local_path).unlink(missing_ok=True)


if __name__ == "__main__":
    run_once()
