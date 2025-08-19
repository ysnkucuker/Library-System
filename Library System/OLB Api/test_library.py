import pytest
import os
import json
from library import Library
from book import Book


# --- Mock Response Sınıfı ---
class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("API Error")


# --- ADD BOOK TESTLERİ ---
def test_add_book_success(monkeypatch, tmp_path):
    """Başarılı kitap ekleme testi"""

    # Mock httpx.get fonksiyonu
    def mock_get(url, *args, **kwargs):
        if "isbn" in url:
            return MockResponse({
                "title": "Test Book",
                "authors": [{"key": "/authors/OL123"}]
            }, 200)
        elif "/authors/OL123.json" in url:
            return MockResponse({"name": "Test Author"}, 200)
        return MockResponse({}, 404)

    monkeypatch.setattr("httpx.get", mock_get)

    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))
    book = lib.add_book("1234567890")

    assert isinstance(book, Book)
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"


def test_add_book_not_found(monkeypatch, tmp_path):
    """Kitap bulunamadığında None dönmeli"""

    def mock_get(url, *args, **kwargs):
        return MockResponse({}, 404)

    monkeypatch.setattr("httpx.get", mock_get)

    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))
    book = lib.add_book("0000000000")

    assert book is None


# --- REMOVE BOOK TESTİ ---
def test_remove_book(tmp_path):
    """Kitap silme testi"""

    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))

    # Kütüphaneye sahte kitap ekle
    book1 = Book("Book1", "Author1", "111")
    book2 = Book("Book2", "Author2", "222")
    lib.books = [book1, book2]
    lib.save_books()

    # Silme işlemi
    lib.remove_book("111")

    # Dosyadan tekrar yükle ve doğrula
    lib.load_books()
    assert len(lib.books) == 1
    assert lib.books[0].isbn == "222"


# --- FIND BOOK TESTİ ---
def test_find_book(tmp_path):
    """ISBN ile kitap bulma testi"""

    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))

    book = Book("Book1", "Author1", "111")
    lib.books = [book]
    lib.save_books()

    found = lib.find_book("111")
    not_found = lib.find_book("999")

    assert found.title == "Book1"
    assert not_found is None


# --- LOAD & SAVE BOOKS TESTİ ---
def test_load_and_save_books(tmp_path):
    """Dosya okuma/yazma testi"""

    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))

    book = Book("Saved Book", "Saved Author", "333")
    lib.books = [book]
    lib.save_books()

    # Yeni Library nesnesi oluşturup tekrar yükle
    lib2 = Library(str(test_file))
    assert len(lib2.books) == 1
    assert lib2.books[0].title == "Saved Book"
