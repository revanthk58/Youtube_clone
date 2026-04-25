from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import os
import yt_dlp
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 Auto-find Frontend.html anywhere in project
def find_html_file(filename):
    for root, dirs, files in os.walk(BASE_DIR):
        if filename in files:
            return os.path.join(root, filename)
    return None

@app.get("/", response_class=HTMLResponse)
def home():
    file_path = find_html_file("Frontend.html")

    if not file_path:
        return "<h2>Frontend.html NOT FOUND ❌</h2>"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/download")
async def download_video(link: str = Form(...)):
    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(BASE_DIR, filename)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    return FileResponse(
        path=os.path.join(BASE_DIR, filename),
        media_type="application/octet-stream",
        filename=filename
    )
