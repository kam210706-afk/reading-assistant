import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "books.json"


def load_books():
    """Загружает книги из JSON-файла."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise TypeError("Файл с книгами должен содержать список.")

        return data

    except (json.JSONDecodeError, OSError, ValueError, TypeError) as error:
        raise RuntimeError(f"Не удалось загрузить книги: {error}") from error


def save_books(books):
    """Сохраняет книги в JSON-файл."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(books, file, ensure_ascii=False, indent=4)

    except OSError as error:
        raise RuntimeError(f"Не удалось сохранить книги: {error}") from error
