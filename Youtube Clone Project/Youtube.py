from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/download")
async def download_video(link: str = Form(...)):
    # Generate a unique filename using the first 15 characters of the link
    sanitized_link = link.replace("https://", "").replace("http://", "").replace("/", "_")  # Sanitize link for filename
    filename = f"video-{sanitized_link[:15]}.mp4"

    youtube_dl_options = {
        "format": "b",
        "out": os.path.join(cur_directory, filename)
    }
    
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])
    
    return {"message": "Download complete", "filename": filename}
