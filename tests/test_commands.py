import commands


def test_show_help(capsys):
    commands.show_help()
    output = capsys.readouterr().out

    assert "add - добавить книгу" in output
    assert "exit - выйти из программы" in output


def test_handle_add_valid(monkeypatch, capsys):
    answers = iter(["1984", "Джордж Оруэлл"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    added = []
    monkeypatch.setattr(
        commands,
        "add_book",
        lambda title, author: added.append((title, author)),
    )

    commands.handle_add()

    assert added == [("1984", "Джордж Оруэлл")]
    assert "успешно добавлена" in capsys.readouterr().out


def test_handle_add_empty_title(monkeypatch, capsys):
    answers = iter(["", "Джордж Оруэлл"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    commands.handle_add()

    assert "не должны быть пустыми" in capsys.readouterr().out


def test_handle_list_empty(monkeypatch, capsys):
    monkeypatch.setattr(commands, "get_books", list)

    commands.handle_list()

    assert "Список книг пока пуст" in capsys.readouterr().out


def test_handle_list_with_books(monkeypatch, capsys):
    monkeypatch.setattr(
        commands,
        "get_books",
        lambda: [
            {
                "title": "1984",
                "author": "Джордж Оруэлл",
                "status": "Читаю",
            }
        ],
    )

    commands.handle_list()
    output = capsys.readouterr().out

    assert "1984" in output
    assert "Джордж Оруэлл" in output
    assert "Читаю" in output


def test_handle_status_empty(monkeypatch, capsys):
    monkeypatch.setattr(commands, "get_books", list)

    commands.handle_status()

    assert "Сначала добавьте книгу" in capsys.readouterr().out


def test_handle_status_invalid_book_number(monkeypatch, capsys):
    monkeypatch.setattr(
        commands,
        "get_books",
        lambda: [{"title": "1984", "author": "Оруэлл", "status": "Читаю"}],
    )
    monkeypatch.setattr("builtins.input", lambda _: "abc")

    commands.handle_status()

    assert "необходимо ввести число" in capsys.readouterr().out


def test_handle_status_invalid_status_number(monkeypatch, capsys):
    monkeypatch.setattr(
        commands,
        "get_books",
        lambda: [{"title": "1984", "author": "Оруэлл", "status": "Читаю"}],
    )
    answers = iter(["1", "abc"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    commands.handle_status()

    assert "необходимо ввести число" in capsys.readouterr().out


def test_handle_status_out_of_range(monkeypatch, capsys):
    monkeypatch.setattr(
        commands,
        "get_books",
        lambda: [{"title": "1984", "author": "Оруэлл", "status": "Читаю"}],
    )
    answers = iter(["1", "9"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    commands.handle_status()

    assert "такого статуса нет" in capsys.readouterr().out


def test_handle_status_success(monkeypatch, capsys):
    monkeypatch.setattr(
        commands,
        "get_books",
        lambda: [{"title": "1984", "author": "Оруэлл", "status": "Читаю"}],
    )
    monkeypatch.setattr(
        commands,
        "update_book_status",
        lambda index, status: index == 0 and status == "Прочитана",
    )

    answers = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    commands.handle_status()

    assert "успешно изменён" in capsys.readouterr().out
