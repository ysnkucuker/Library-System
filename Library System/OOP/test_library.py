import os
import pytest
from book import Book
from library import Library

TEST_FILE = "test_library.json"

@pytest.fixture
def test_library():
    # Her test için temiz bir dosya
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    lib = Library(TEST_FILE)
    return lib

def test_add_book(test_library):
    book = Book("The Hobbit", "J.R.R. Tolkien", "12345")
    test_library.add_book(book)
    assert len(test_library.books) == 1
    assert test_library.books[0].title == "The Hobbit"

def test_remove_book(test_library):
    book = Book("1984", "George Orwell", "67890")
    test_library.add_book(book)
    test_library.remove_book("67890")
    assert len(test_library.books) == 0

def test_find_book(test_library):
    book = Book("Dune", "Frank Herbert", "11111")
    test_library.add_book(book)
    found = test_library.find_book("11111")
    assert found is not None
    assert found.title == "Dune"

def test_list_books(capsys, test_library):
    book = Book("Sefiller", "Victor Hugo", "22222")
    test_library.add_book(book)
    test_library.list_books()
    captured = capsys.readouterr()
    assert "Sefiller" in captured.out
