from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(
    directory="app/templates"
)

from app.routers.part1_router import (
    router as part1_router
)

app = FastAPI(
    title="TOEIC AI",
    version="1.0.0"
)

app.include_router(
    part1_router
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

@app.get("/")
def root():

    return {
        "message": "TOEIC AI is running"
    }

@app.get("/part1")
def part1_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="part1.html"
    )