from storage import load_books, save_books

STATUSES = ["Запланирована", "Читаю", "Прочитана"]

books = load_books()


def add_book(title, author):
    """Добавляет новую книгу в список."""
    book = {
        "title": title,
        "author": author,
        "status": STATUSES[0],
    }

    books.append(book)

    try:
        save_books(books)
    except RuntimeError:
        books.remove(book)
        raise

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

    old_status = books[book_index]["status"]
    books[book_index]["status"] = new_status

    try:
        save_books(books)
    except RuntimeError:
        books[book_index]["status"] = old_status
        raise

    return True
