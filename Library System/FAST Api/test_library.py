import pytest
from fastapi.testclient import TestClient
from api import app, library, Book

# --- Test Client ---
client = TestClient(app)

# --- Mock Library.add_book fonksiyonu ---
class MockBook:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

def mock_add_book_success(isbn):
    return MockBook("Test Book", "Test Author", isbn)

def mock_add_book_fail(isbn):
    return None

# ----------------------------
# GET /books testleri
# ----------------------------
def test_get_books_empty(monkeypatch):
    # Library.books boş
    monkeypatch.setattr(library, "books", [])
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_get_books_with_data(monkeypatch):
    monkeypatch.setattr(library, "books", [MockBook("Book1", "Author1", "111")])
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Book1"
    assert data[0]["author"] == "Author1"
    assert data[0]["isbn"] == "111"

# ----------------------------
# POST /books testleri
# ----------------------------
def test_post_books_success(monkeypatch):
    monkeypatch.setattr(library, "add_book", mock_add_book_success)
    response = client.post("/books", json={"isbn": "1234567890"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["isbn"] == "1234567890"

def test_post_books_fail(monkeypatch):
    monkeypatch.setattr(library, "add_book", mock_add_book_fail)
    response = client.post("/books", json={"isbn": "0000000000"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı veya eklenemedi."

# ----------------------------
# DELETE /books/{isbn} testleri
# ----------------------------
def test_delete_books_success(monkeypatch):
    mock_book = MockBook("Book1", "Author1", "111")
    monkeypatch.setattr(library, "find_book", lambda isbn: mock_book)
    monkeypatch.setattr(library, "remove_book", lambda isbn: True)
    response = client.delete("/books/111")
    assert response.status_code == 200
    assert response.json()["message"] == "111 numaralı kitap silindi."

def test_delete_books_not_found(monkeypatch):
    monkeypatch.setattr(library, "find_book", lambda isbn: None)
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı."
