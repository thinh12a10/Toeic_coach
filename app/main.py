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
from app.routers.part2_router import (
    router as part2_router
)
from app.routers.part3_router import (
    router as part3_router
)

app = FastAPI(
    title="TOEIC AI",
    version="1.0.0"
)

app.include_router(
    part1_router
)
app.include_router(
    part2_router
)
app.include_router(
    part3_router
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

@app.get("/")
def root(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/part1")
def part1_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="part1.html"
    )

@app.get("/part2")
def part2_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="part2.html"
    )

@app.get("/part3")
def part3_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="part3.html"
    )