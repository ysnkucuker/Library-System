from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from library import Library
from book import Book

app = FastAPI(title="Library API", version="1.0")

# JSON dosyasına bağlı Library instance
library = Library("library.json")

# --- Pydantic Modeller ---
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNRequest(BaseModel):
    isbn: str

# --- Endpoint'ler ---
@app.get("/books", response_model=List[BookModel])
def get_books():
    return [BookModel(**book.__dict__) for book in library.books]

@app.post("/books", response_model=BookModel)
def add_book(isbn_req: ISBNRequest):
    book = library.add_book(isbn_req.isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya eklenemedi.")
    return BookModel(**book.__dict__)

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    found = library.find_book(isbn)
    if not found:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    library.remove_book(isbn)
    return {"message": f"{isbn} numaralı kitap silindi."}
