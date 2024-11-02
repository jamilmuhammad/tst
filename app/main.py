from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)

@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.update_author(db, author_id, author)

@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(db, author_id)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)

@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_author_books(author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_author_books(db, author_id, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)