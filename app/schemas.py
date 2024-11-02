from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    description: str
    publish_date: date
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class AuthorBase(BaseModel):
    name: str
    bio: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True