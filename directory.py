import os.path

from records import Record
from tabulate import tabulate


class Directory:
    def __init__(self):
        """
        Конструктор для создания справочника.
        """
        self.records = []
        self.next_pk = 1

    def add_record(self, record: Record):
        """
        Добавление записи в справочник.
        :param record: Запись
        """
        while any(r.pk == self.next_pk for r in self.records):
            self.next_pk += 1
        record.pk = self.next_pk
        self.records.append(record)
        self.next_pk += 1

    def edit_record(self, pk, **kwargs):
        """
        Редактирование существующей записи.
        :param pk: Первичный ключ записи
        :param kwargs: Словарь с новыми значениями атрибутов
        """
        record = self.get_record_by_pk(pk)
        if record:
            record.edit(**kwargs)
        else:
            print("Запись с указанным PK не найдена.")

    def get_record_by_pk(self, pk):
        """
        Получение записи по её PK.
        :param pk: Первичный ключ записи
        :return: Объект записи или None, если запись не найдена
        """
        for record in self.records:
            if record.pk == pk:
                return record
        return None

    def search_records(self, **kwargs):
        """
        Поиск записей по характеристикам.
        :param kwargs: Словарь с характеристиками для поиска
        :return: Список кортежей (PK, запись) найденных записей
        """
        matching_records = []
        for record in self.records:
            match = False
            for key, value in kwargs.items():
                record_value = getattr(record, key, None)
                if record_value and value.lower() in record_value.lower():
                    match = True
                    break
            if match:
                matching_records.append((record.pk, record))
        return matching_records

    def print_page(self, page_number, page_size=10):
        """
        Вывод страницы с записями на экран.
        :param page_number: Номер страницы
        :param page_size: Количество записей на странице
        """
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        records_to_display = self.records[start_index:end_index]

        table_data = []
        for record in records_to_display:
            table_data.append([record.pk, f"{record.surname} {record.name} {record.patronymic}",
                               record.organization, record.work_phone, record.cell_phone])

        headers = ["PK", "ФИО", "Организация", "Рабочий телефон", "Сотовый телефон"]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def save_to_file(self, filename='yellow_pages.txt', ):
        """
        Сохранение данных справочника в текстовый файл.
        :param filename: Имя файла, по умолчанию в корень папки с программой в ффайл yellow_pages.txt
        """
        with open(filename, "w", encoding="utf-8") as file:
            for record in self.records:
                file.write(f"{record.pk}; {record.surname}; {record.name}; {record.patronymic}; {record.organization}; {record.work_phone}; {record.cell_phone}\n")

    @classmethod
    def load_from_file(cls, filename='yellow_pages.txt'):
        """
        Загрузка данных справочника из текстового файла.
        :param filename: Имя файла
        :return: Экземпляр справочника с загруженными данными
        """
        directory = cls()
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    pk, surname, name, patronymic, organization, work_phone, cell_phone = line.strip().split("; ")
                    record = Record(surname, name, patronymic, organization, work_phone, cell_phone)
                    directory.add_record(record)
        return directory
