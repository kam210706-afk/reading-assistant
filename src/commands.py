from books import STATUSES, add_book, get_books, update_book_status


def show_help():
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("add - добавить книгу")
    print("list - показать список книг")
    print("status - изменить статус книги")
    print("help - показать помощь")
    print("exit - выйти из программы")

def handle_add():
    """Запрашивает данные и добавляет книгу."""
    title = input("Название книги: ").strip()
    author = input("Автор книги: ").strip()

    if not title or not author:
        print("Ошибка: название и автор не должны быть пустыми.")
        return

    add_book(title, author)
    print("Книга успешно добавлена!")

def handle_list():
    """Показывает все книги."""
    books = get_books()

    if not books:
        print("Список книг пока пуст.")
        return

    print("\nВаш список книг:")
    for index, book in enumerate(books, start=1):
        print(f"{index}. {book['title']} — {book['author']}")
        print(f"   Статус: {book['status']}")

def handle_status():
    """Изменяет статус выбранной книги."""
    books = get_books()

    if not books:
        print("Сначала добавьте книгу.")
        return

    handle_list()

    try:
        book_index = int(input("Введите номер книги: ")) - 1
    except ValueError:
        print("Ошибка: необходимо ввести число.")
        return

    print("\nВыберите новый статус:")
    for index, status in enumerate(STATUSES, start=1):
        print(f"{index}. {status}")

    try:
        status_index = int(input("Введите номер статуса: ")) - 1
    except ValueError:
        print("Ошибка: необходимо ввести число.")
        return

    if status_index < 0 or status_index >= len(STATUSES):
        print("Ошибка: такого статуса нет.")
        return

    if update_book_status(book_index, STATUSES[status_index]):
        print("Статус книги успешно изменён!")
    else:
        print("Ошибка: книги с таким номером нет.")