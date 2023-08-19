from directory import Directory
from art import tprint
from actions import add_record, edit_record, search_records, display_records


def main():
    """
    Основная функция программы, выполняющая цикл работы со справочником.
    """
    directory = Directory.load_from_file()
    tprint("YellowPagesJunior", font="standard")

    while True:
        print("___" * 30)
        print("Выберите действие:")
        print("1. Добавить запись")
        print("2. Редактировать запись")
        print("3. Поиск записей")
        print("4. Вывести записи")
        print("5. Выйти")
        choice = input("Введите номер действия> ")

        if choice == '1':
            add_record(directory)
        elif choice == '2':
            edit_record(directory)
        elif choice == '3':
            search_records(directory)
        elif choice == '4':
            display_records(directory)
        elif choice == '5':
            directory.save_to_file()
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
