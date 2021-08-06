from typing import List, Optional
from pydantic import BaseModel

class RepositoryBase(BaseModel):
    name: str
    link: str

class RepositoryCreate(RepositoryBase):
    pass

class Repository(RepositoryBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    name: str
    username: str
    image: str
    is_active: bool
    respositories: List[Repository] = []
    class Config:
        orm_mode = True