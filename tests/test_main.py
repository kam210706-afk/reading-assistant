import main


def test_main_exit(monkeypatch, capsys):
    answers = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.main()

    output = capsys.readouterr().out

    assert "READING ASSISTANT" in output
    assert "Спасибо за использование Reading Assistant!" in output


def test_main_commands(monkeypatch, capsys):
    answers = iter(["help", "unknown", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.main()

    output = capsys.readouterr().out

    assert "Доступные команды" in output
    assert "Неизвестная команда" in output


def test_main_keyboard_interrupt(monkeypatch, capsys):
    def interrupt(_):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", interrupt)

    main.main()

    assert "Работа программы завершена" in capsys.readouterr().out


def test_main_eof_error(monkeypatch, capsys):
    def end_input(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", end_input)

    main.main()

    assert "Работа программы завершена" in capsys.readouterr().out
