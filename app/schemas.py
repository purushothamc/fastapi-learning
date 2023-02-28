from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode =True