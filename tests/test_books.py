import pytest

import books
import storage


@pytest.fixture
def clean_books(tmp_path, monkeypatch):
    """Создаёт временное хранилище для каждого теста."""
    data_file = tmp_path / "books.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)
    monkeypatch.setattr(books, "books", [])

    return data_file


def test_load_books_without_file(clean_books):
    assert storage.load_books() == []


def test_save_and_load_books(clean_books):
    data = [
        {
            "title": "1984",
            "author": "Джордж Оруэлл",
            "status": "Читаю",
        }
    ]

    storage.save_books(data)

    assert storage.load_books() == data


def test_load_invalid_json(clean_books):
    clean_books.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(RuntimeError):
        storage.load_books()


def test_load_invalid_data_format(clean_books):
    clean_books.write_text('{"title": "1984"}', encoding="utf-8")

    with pytest.raises(RuntimeError):
        storage.load_books()


def test_add_book(clean_books):
    book = books.add_book("1984", "Джордж Оруэлл")

    assert book["title"] == "1984"
    assert book["author"] == "Джордж Оруэлл"
    assert book["status"] == "Запланирована"
    assert storage.load_books() == [book]


def test_get_books(clean_books):
    books.books.append(
        {
            "title": "1984",
            "author": "Джордж Оруэлл",
            "status": "Читаю",
        }
    )

    assert len(books.get_books()) == 1


def test_update_book_status(clean_books):
    books.add_book("1984", "Джордж Оруэлл")

    result = books.update_book_status(0, "Читаю")

    assert result is True
    assert books.get_books()[0]["status"] == "Читаю"
    assert storage.load_books()[0]["status"] == "Читаю"


def test_update_invalid_book_index(clean_books):
    books.add_book("1984", "Джордж Оруэлл")

    assert books.update_book_status(5, "Читаю") is False
    assert books.update_book_status(-1, "Читаю") is False


def test_update_invalid_status(clean_books):
    books.add_book("1984", "Джордж Оруэлл")

    assert books.update_book_status(0, "Неизвестный статус") is False


def test_save_error_rolls_back_added_book(clean_books, monkeypatch):
    def fail_save(data):
        raise RuntimeError("Ошибка сохранения")

    monkeypatch.setattr(books, "save_books", fail_save)

    with pytest.raises(RuntimeError):
        books.add_book("1984", "Джордж Оруэлл")

    assert books.get_books() == []


def test_save_error_rolls_back_status(clean_books, monkeypatch):
    books.add_book("1984", "Джордж Оруэлл")

    def fail_save(data):
        raise RuntimeError("Ошибка сохранения")

    monkeypatch.setattr(books, "save_books", fail_save)

    with pytest.raises(RuntimeError):
        books.update_book_status(0, "Читаю")

    assert books.get_books()[0]["status"] == "Запланирована"


def test_save_error(clean_books, tmp_path, monkeypatch):
    missing_file = tmp_path / "missing" / "books.json"
    monkeypatch.setattr(storage, "DATA_FILE", missing_file)

    with pytest.raises(RuntimeError):
        storage.save_books([])
