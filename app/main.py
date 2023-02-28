from typing import Optional
from fastapi import FastAPI
import psycopg2
from random import randrange
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="root", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection is successfull")
except Exception as e:
    print("Unable to connect to Database")
    print("Error:", e)


all_posts = [
    {
        "title": "blog post #1",
        "content": "blog post #1",
        "id": 1
    },
    {
        "title": "blog post #2",
        "content": "blog post #2",
        "id": 2
    },
]

def find_posts(id):
    abcd = None
    for post in all_posts:
        if post["id"] == id:
            return post
    return abcd

def find_post_index(id):
    index = None
    for idx, post in enumerate(all_posts):
        if post["id"] == id:
            return idx
    return index

app.include_router(user.router)
app.include_router(post.router)
