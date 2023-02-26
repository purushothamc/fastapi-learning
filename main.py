from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel 
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    post = None
    for post in all_posts:
        if post["id"] == id:
            return post
    return post

@app.get("/posts")
def get_posts():
    return {"data": all_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000)
    all_posts.append(post.dict())
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_posts(int(id))
    return {"post": post}
 

