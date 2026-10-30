import json
from pathlib import Path

STATUSES = ["Запланирована", "Читаю", "Прочитана"]

DATA_FILE = Path(__file__).resolve().parent.parent / "books.json"

def load_books():
    """Загружает список книг из JSON-файла."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

books = load_books()

def save_books():
    """Сохраняет список книг в JSON-файл."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)

def add_book(title, author):
    """Добавляет новую книгу в список."""
    book = {
        "title": title,
        "author": author,
        "status": STATUSES[0]
    }

    books.append(book)
    save_books()
    return book

def get_books():
    """Возвращает список всех книг."""
    return books

def update_book_status(book_index, new_status):
    """Изменяет статус выбранной книги."""
    if book_index < 0 or book_index >= len(books):
        return False

    if new_status not in STATUSES:
        return False

    books[book_index]["status"] = new_status
    save_books()
    return True