from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String)
    birth_date = Column(Date)
    
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    publish_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
    
    author = relationship("Author", back_populates="books")