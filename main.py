from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
    card = [
                [
                    {
                        "name": "Siegwurm-Nova_X",
                        "img": "https://static.wikia.nocookie.net/battle-spirits/images/e/e8/Siegwurm-Nova_X.jpg",
                        "url": "https://battle-spirits.fandom.com/wiki/Siegwurm-Nova_X"
                    },
                    {
                        "name": "CB18-X04",
                        "img": "https://static.wikia.nocookie.net/battle-spirits/images/e/eb/CB18-X04.png",
                        "url": "https://battle-spirits.fandom.com/wiki/CB18-X04"
                    }
                ]
            ]
    return templates.TemplateResponse("index.html", {"request": request, 
                                                        "card": card})