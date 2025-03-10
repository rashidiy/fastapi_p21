from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from admin import ProductAdmin, CategoryAdmin
from db import engine, init_db, destroy_db
from models import Category, Product
app = FastAPI()

admin = Admin(app, engine)
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)

app.mount("/static", StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

users = [
    {
        "id": 1,
        "full_name": "Botirjon",
        "position": "Frontend developer",
        "projects": 45,
        "tasks": 15,
        "completed_projects": 6,
        "followers": 76
    },
    {
        "id": 2,
        "full_name": "Gayratjon",
        "position": "Backend engineer",
        "projects": 435,
        "tasks": 154,
        "completed_projects": 66,
        "followers": 7
    },
    {
        "id": 3,
        "full_name": "Nadia Carmichael",
        "position": "Lead Developer",
        "projects": 2,
        "tasks": 64,
        "completed_projects": 16,
        "followers": 842
    },
]


@app.on_event("startup")
def on_startup():
    init_db()


@app.on_event("shutdown")
def on_startup():
    pass
    # destroy_db()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = {
        'users': users
    }
    return templates.TemplateResponse(request, 'user-list.html', context)


# https://bootdey.com/
@app.get("/users/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    _user = None
    for user in users:
        if user['id'] == id:
            _user = user

    context = {
        'user': _user
    }
    return templates.TemplateResponse(request, 'user-detail.html', context)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
