from tabulate import tabulate
from records import validate_phone, validate_name, Record
from directory import Directory



def input_with_validation(prompt, validation_func, skip_spaces=False):
    """
    Запрос ввода пользователя с проверкой вводимых данных с использованием указанной функции проверки.
    :param prompt: Подсказка для пользователя
    :param validation_func: Функция валидации для проверки пользовательского ввода
    :param skip_spaces: Не проверять, если введенное значение пусто
    :return: Проверенный пользовательский ввод или None
    """
    while True:
        value = input(prompt + ": ")
        if skip_spaces and value == "":
            break
        try:
            value = validation_func(value)
            return value
        except ValueError as e:
            print("Ошибка:", e)
            retry = input("Хотите попробовать снова? (y/n): ").lower()
            if retry != 'y':
                break


def add_record(directory):
    """
    Функция для добавления новой записи в справочник, с запросом информации у пользователя по каждому полю.
    :param directory: Справочник, в который добавляется запись
    """
    print("___" * 30)
    print("Добавление новой записи:")

    surname = input_with_validation("Фамилия", validate_name)
    if surname is None:
        return

    name = input_with_validation("Имя", validate_name)
    if name is None:
        return

    patronymic = input_with_validation("Отчество", validate_name)
    if patronymic is None:
        return

    organization = input("Название организации: ")
    work_phone = input_with_validation("Рабочий телефон", validate_phone)
    if work_phone is None:
        return

    cell_phone = input_with_validation("Личный телефон (сотовый)", validate_phone)
    if cell_phone is None:
        return

    try:
        record = Record(surname, name, patronymic, organization, work_phone, cell_phone)
        directory.add_record(record)
        directory.save_to_file()
        print("Запись успешно добавлена.")
        directory = Directory.load_from_file()
    except ValueError as e:
        print("Ошибка:", e)


def edit_record(directory):
    """
    Функция для определения записи для изменения, с возможностью поиска записи по ключевому слову или PK
    :param directory: Справочник, в котором происходит редактирование
    """
    print("___" * 30)
    print("Редактирование записи:")

    choice = input("Выберите способ поиска: \n1. Поиск по имени\n2. Ввод номера записи (PK)\n")

    if choice == '1':
        search_term = input("Введите часть ФИО, названия организации или номера телефона для поиска записей: ")
        matching_records = directory.search_records(surname=search_term,
                                                    name=search_term,
                                                    patronymic=search_term,
                                                    organization=search_term,
                                                    work_phone=search_term,
                                                    cell_phone=search_term
                                                    )

        if not matching_records:
            print("___" * 30)
            print("Записи не найдены.")
            return

        print("___" * 30)
        print("Найденные записи:")

        results_table = []
        for index, (_, record) in enumerate(matching_records, start=1):
            results_table.append([index, record.surname, record.name, record.patronymic,
                                  record.organization, record.work_phone, record.cell_phone])
        headers = ["#", "Фамилия", "Имя", "Отчество", "Название организации", "Рабочий телефон",
                   "Личный телефон (сотовый)"]
        results_table_formatted = tabulate(results_table, headers=headers, tablefmt="pretty")
        print(results_table_formatted)

        try:
            record_index = int(input("Введите номер записи (#), которую хотите отредактировать: ")) - 1
            if 0 <= record_index < len(matching_records):
                edit_selected_record(directory, matching_records[record_index])
            else:
                print("___" * 30)
                print("Недопустимый номер записи.")
        except ValueError:
            print("___" * 30)
            print("Неверный формат номера записи.")

    elif choice == '2':
        try:
            print("___" * 30)
            pk = int(input("Введите номер записи (PK), которую хотите отредактировать: "))
            record = directory.get_record_by_pk(pk)
            if record:
                edit_selected_record(directory, (pk, record))
            else:
                print("___" * 30)
                print("Запись с указанным ПК не найдена.")
        except ValueError:
            print("___" * 30)
            print("Неверный формат номера записи.")
    else:
        print("___" * 30)
        print("Недопустимый выбор.")


def edit_selected_record(directory, record_tuple):
    """
    Функция для редактирования выбранной записи в справочнике, с запросом информации у пользователя по каждому полю.
    :param directory: Справочник, в котором происходит редактирование
    :param record_tuple: Кортеж, содержащий номер PK и запись для редактирования
    """
    pk, record = record_tuple
    print("___" * 30)
    print(f"Редактирование записи: {record}")
    new_values = {}
    print("Введите новые значения (оставьте пустым, чтобы оставить без изменений):")

    for field, prompt, validation_func in [
        ("surname", "Фамилия", validate_name),
        ("name", "Имя", validate_name),
        ("patronymic", "Отчество", validate_name),
        ("organization", "Название организации", None),
        ("work_phone", "Рабочий телефон", validate_phone),
        ("cell_phone", "Личный телефон (сотовый)", validate_phone)
    ]:
        current_value = getattr(record, field)
        if validation_func is None:
            new_value = input(f"{prompt} (текущее значение: {current_value}): ")
            if new_value == "":
                continue
        else:
            new_value = input_with_validation(f"{prompt} (текущее значение: {current_value})", validation_func,
                                              skip_spaces=True)
            if new_value == "":
                continue
        if new_value is not None:
            new_values[field] = new_value

    directory.edit_record(pk, **new_values)
    directory.save_to_file()
    print("___" * 30)
    print("Запись успешно отредактирована.")
    directory = Directory.load_from_file()


def search_records(directory):
    """
    Функция для поиска записей в справочнике, с запросом искомого слова у пользователя.
    :param directory: Справочник, в котором происходит поиск
    """
    print("___" * 30)
    print("Поиск записей:")
    search_term = input("Введите слово для поиска: ")
    results = directory.search_records(surname=search_term, name=search_term, patronymic=search_term,
                                       organization=search_term, work_phone=search_term, cell_phone=search_term)
    if results:
        table_data = []
        for pk, record in results:
            table_data.append([pk, f"{record.surname} {record.name} {record.patronymic}",
                               record.organization, record.work_phone, record.cell_phone])

        headers = ["PK", "ФИО", "Организация", "Рабочий телефон", "Личный телефон"]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("Записи не найдены.")


def display_records(directory):
    """
    Функция для вывода записей из справочника с опциями навигации и настройки.
    :param directory: Справочник, из которого происходит вывод записей
    """
    total_records = len(directory.records)
    records_per_page = 10  # Default records per page
    total_pages = (total_records + records_per_page - 1) // records_per_page
    page_number = 1  # Default page number

    while True:
        print("___" * 30)
        print(f"Всего записей: {total_records}", f"Всего страниц: {total_pages}")
        print("Опции:")
        print("1. Задать количество записей на странице")
        if page_number < total_pages:
            print("2. Перейти к следующей странице")
        if page_number > 1:
            print("3. Перейти к предыдущей странице")
        if total_pages > 1:
            print("4. Ввести номер страницы")
        print("5. Выйти")
        option = input("Введите опцию: ")

        if option == "1":
            records_per_page = int(input("Введите количество записей на странице: "))
            total_pages = (total_records + records_per_page - 1) // records_per_page
        elif option == "2" and page_number < total_pages:
            page_number += 1
        elif option == "3" and page_number > 1:
            page_number -= 1
        elif option == "4" and total_pages > 1:
            new_page_number = int(input("Введите номер страницы: "))
            if 1 <= new_page_number <= total_pages:
                page_number = new_page_number
            else:
                print("___" * 30)
                print("Недопустимый номер страницы.")
        elif option == "5":
            break

        if option in {"1", "2", "3", "4"}:
            print("___" * 30)
            print("Вывод записей:")
            print(f"Всего записей: {total_records}")

            start_index = (page_number - 1) * records_per_page
            end_index = min(start_index + records_per_page, total_records)

            print(f"Страница {page_number}/{total_pages} - Записи {start_index + 1}-{end_index}:")

            directory.print_page(page_number, page_size=records_per_page)

            print(f"Страница {page_number}/{total_pages} - Записи {start_index + 1}-{end_index}:")
