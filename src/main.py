from commands import handle_add, handle_list, handle_status, show_help


def main():
    """Запускает помощника по чтению."""
    print("=" * 35)
    print("       READING ASSISTANT")
    print("=" * 35)
    print("Добро пожаловать в помощник по чтению!")

    show_help()

    while True:
        command = input("\nВведите команду: ").strip().lower()

        if command == "add":
            handle_add()

        elif command == "list":
            handle_list()

        elif command == "status":
            handle_status()

        elif command == "help":
            show_help()

        elif command == "exit":
            print("Спасибо за использование Reading Assistant!")
            break

        else:
            print("Неизвестная команда. Введите help для просмотра команд.")


if __name__ == "__main__":
    main()
