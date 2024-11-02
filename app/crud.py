from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from . import cache
from datetime import timedelta

def get_author(db: Session, author_id: int):
    # Try to get from cache first
    cache_key = f"author:{author_id}"
    cached_author = cache.get_cache(cache_key)
    if cached_author:
        return cached_author
        
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author:
        cache.set_cache(cache_key, author)
    return author

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    cache.set_cache(f"author:{author_id}", db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    author = get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(author)
    db.commit()
    cache.redis_client.delete(f"author:{author_id}")
    return author

def get_book(db: Session, book_id: int):
    # Try to get from cache first
    cache_key = f"book:{book_id}"
    cached_book = cache.get_cache(cache_key)
    if cached_book:
        return cached_book
        
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        cache.set_cache(cache_key, book)
    return book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    cache.set_cache(f"book:{book_id}", db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    cache.redis_client.delete(f"book:{book_id}")
    return book

def get_author_books(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )