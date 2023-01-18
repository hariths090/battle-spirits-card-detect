from fastapi import FastAPI, Request, File, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai import detect_card_filename, detect_card_filebyte
import numpy as np
import cv2
app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/card", StaticFiles(directory="card"), name="card")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
    card = detect_card_filename()
    return templates.TemplateResponse("index.html", {"request": request, 
                                                        "card": card})

@app.post("/upload/")
async def get_body(file: bytes = File(...), save: bool = False):
    if save == True:
        open("./images/source.jpg", "wb").write(file)
        return {"result": detect_card_filename()}
    else:
        return {"result": detect_card_filebyte(file)}