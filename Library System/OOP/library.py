import json
import os
from book import Book

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def add_book(self, book: Book):
        # ISBN benzersiz olsun
        if any(b.isbn == book.isbn for b in self.books):
            print("Bu ISBN ile bir kitap zaten mevcut!")
            return
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                self.save_books()
                print(f"{book.title} silindi.")
                return
        print("Kitap bulunamadı.")

    def list_books(self):
        if not self.books:
            print("Kütüphane boş.")
        for book in self.books:
            print(book)

    def find_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.books = [Book(**book_data) for book_data in data]
                except json.JSONDecodeError:
                    self.books = []
        else:
            self.books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.__dict__ for book in self.books], f, indent=4, ensure_ascii=False)
