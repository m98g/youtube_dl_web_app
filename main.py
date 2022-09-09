from __future__ import unicode_literals
import youtube_dl
import os
from fastapi import Request
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from form import downloadform
from glob import glob
from fastapi.background import BackgroundTasks


app = FastAPI()
templates = Jinja2Templates(directory="templates")

ydl_opts = {'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse("base.html", {"request": request})

def remove_file(path: str) -> None:
    os.unlink(path)

@app.post("/download")
async def form_func(request: Request, background_tasks: BackgroundTasks):
    form = downloadform(request)
    await form.load_data()
    os.chdir("/tmp")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([form.url])
    file = glob('*.mp3')
    path_ = file[0]
    background_tasks.add_task(remove_file, path_)
    return FileResponse(path=path_, media_type='application/octet-stream', filename=f"{path_}.mp3")
    