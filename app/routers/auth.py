from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login_user(credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    # successful login
    # create JWT token and return
    token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
