from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
from ai import detect_card

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/card", StaticFiles(directory="card"), name="card")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
    card = detect_card()
    return templates.TemplateResponse("index.html", {"request": request, 
                                                        "card": card})