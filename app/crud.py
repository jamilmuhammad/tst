from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from . import models, schemas
from fastapi import HTTPException
from . import cache
from datetime import timedelta

def get_author(db: Session, author_id: int):
    cache_key = f"author:{author_id}"
    cached_author = cache.get_cache(cache_key)
    if cached_author:
        return schemas.Author(**cached_author)
        
    try:
        author = db.query(models.Author).filter(models.Author.id == author_id).first()
        author_data = schemas.Author.from_orm(author).dict()
        cache.set_cache(cache_key, author_data)
        return author
    except NoResultFound:
        return None

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def update_author(db: Session, author_id: int, author_update_data: schemas.AuthorCreate):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    
    if not author:
        return HTTPException("Author not found")

    for key, value in author_update_data.dict(exclude_unset=True).items():
        setattr(author, key, value)
    
    db.commit()
    db.refresh(author)

    cache.set_cache(f"author:{author_id}", schemas.Author.from_orm(author).dict())

    return schemas.Author.from_orm(author)

def delete_author(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(author)
    db.commit()

    cache.redis_client.delete(f"author:{author_id}")
    return schemas.Author.from_orm(author)

def get_book(db: Session, book_id: int):
    cache_key = f"book:{book_id}"
    cached_book = cache.get_cache(cache_key)
    if cached_book:
        return schemas.Book(**cached_book)
        
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        book_data = schemas.Book.from_orm(book).dict()
        cache.set_cache(cache_key, book_data)
        return book
    except NoResultFound:
        return None

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update_data: schemas.BookCreate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        return HTTPException("Book not found")

    for key, value in book_update_data.dict(exclude_unset=True).items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)

    cache.set_cache(f"book:{book_id}", schemas.Book.from_orm(book).dict())

    return schemas.Book.from_orm(book)

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    cache.redis_client.delete(f"book:{book_id}")
    return schemas.Book.from_orm(book)

def get_author_books(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )