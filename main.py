from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from conf.db import engine
from front import urls
from todolist import views, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(views.router, tags=['ToDoList'], prefix='/api')
app.include_router(urls.router, tags=['Front'], prefix='/front')

app.mount("/static", StaticFiles(directory="static"), name="static")


