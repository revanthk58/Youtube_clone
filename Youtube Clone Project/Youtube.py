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

# 🔥 Get correct base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Serve HTML properly
@app.get("/", response_class=HTMLResponse)
def home():
    file_path = os.path.join(BASE_DIR, "Frontend.html")
    
    if not os.path.exists(file_path):
        return {"error": f"Frontend.html not found at {file_path}"}
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# ✅ Download API
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
