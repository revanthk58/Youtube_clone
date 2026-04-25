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

cur_directory = os.getcwd()

# ✅ Serve your existing HTML file
@app.get("/", response_class=HTMLResponse)
def home():
    with open("Frontend.html", "r", encoding="utf-8") as file:
        return file.read()

# ✅ Download API
@app.post("/download")
async def download_video(link: str = Form(...)):
    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(cur_directory, filename)  # FIXED
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    return FileResponse(
        path=filename,
        media_type="application/octet-stream",
        filename=filename
    )
