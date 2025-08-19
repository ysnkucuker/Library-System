import json
import os
import httpx
from book import Book


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.books = [Book(**book_data) for book_data in data]
                except json.JSONDecodeError:
                    # Dosya boş veya geçersiz JSON ise boş liste kullan
                    self.books = []
        else:
            self.books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.__dict__ for book in self.books], f, indent=4)

    def add_book(self, isbn: str):
        """ISBN numarası ile Open Library API'den kitap bilgisi al ve ekle"""
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(url, timeout=10, follow_redirects=True)

            if response.status_code == 404:
                print("Kitap bulunamadı.")
                return None
            response.raise_for_status()

            data = response.json()
            title = data.get("title", "Bilinmeyen Başlık")

            # Authors bilgisi almak için ayrı bir istek gerekebilir
            authors = []
            for author in data.get("authors", []):
                key = author.get("key")
                if key:
                    author_resp = httpx.get(f"https://openlibrary.org{key}.json", timeout=10)
                    if author_resp.status_code == 200:
                        author_name = author_resp.json().get("name", "Bilinmeyen Yazar")
                        authors.append(author_name)

            author = ", ".join(authors) if authors else "Bilinmeyen Yazar"

            book = Book(title, author, isbn)
            self.books.append(book)
            self.save_books()
            print(f"Kitap eklendi: {book}")
            return book

        except httpx.RequestError:
            print("Bağlantı hatası! İnternet bağlantınızı kontrol edin.")
            return None

    def remove_book(self, isbn: str):
        """ISBN numarası aynı olanı eklemeyerek silmiş oluyoruz"""
        self.books = [book for book in self.books if book.isbn != isbn]
        self.save_books()

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
