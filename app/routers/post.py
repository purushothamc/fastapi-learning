

from fastapi import Depends, HTTPException, Response, status, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #post_dict = post.dict()
    #post_dict["id"] = randrange(1, 10000)
    #all_posts.append(post.dict())
    #return {"data": post_dict}
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #post = find_posts(int(id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with {id} doesn't exist")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with {id} doesn't exist"}
    return post
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    #index = find_post_index(int(id))
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with {id} doesn't exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    #all_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #index = find_post_index(int(id))
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post, post.__dict__)

    #if index == None:
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with {id} doesn't exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
 
    """post_dict = post.dict()
    post_dict["id"] = id
    all_posts[index] = post_dict"""

    return post_query.first()
