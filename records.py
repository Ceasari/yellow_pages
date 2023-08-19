import re
import phonenumbers


def validate_name(text):
    """
    Проверка ФИО на корректность. Должны состоять только из букв и допустимо использовать один дефис.
    :param text: Текст для проверки
    :return text: Проверенный текс
    """
    text_with_replaced_letters = text.replace("Ё", "е").replace("ё", "е")
    if not re.match("^[A-Za-zА-Яа-я]+(?:-[A-Za-zА-Яа-я]+)?$", text_with_replaced_letters):
        raise ValueError(f"ФИО может содержать только буквы и один дефис. {text}")
    return text_with_replaced_letters


def validate_phone(phone):
    """
    Проверка телефонного номера.
    :param phone: Номер для валидации
    :return formatted_number: телефон в формате +X-XXX-XXX-XXXX
    """
    digits = re.sub(r'\D', '', phone)

    if len(digits) == 10:
        formatted_number = f"+7-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('8'):
        formatted_number = f"+7-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 11 and digits.startswith('7'):
        formatted_number = f"+7-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 11 and not digits.startswith('7') and not digits.startswith('8'):
        raise ValueError(
            f"Номер телефона '{phone}' должен начинаться с +7 или 8 и состоять из 11 цифр")
    else:
        raise ValueError(
            f"Номер телефона '{phone}' не является корректным номером. Пожалуйста, используйте формат +7-XXX-XXX-XXXX.")

    return formatted_number


class Record:
    def __init__(self, surname, name, patronymic, organization, work_phone, cell_phone):
        """
        Конструктор для создания записи в справочнике.
        :param surname: Фамилия
        :param name: Имя
        :param patronymic: Отчество
        :param organization: Название организации
        :param work_phone: Рабочий телефон
        :param cell_phone: Личный телефон (сотовый)
        """
        self.surname = validate_name(surname)
        self.name = validate_name(name)
        self.patronymic = validate_name(patronymic)
        self.organization = organization
        self.work_phone = validate_phone(work_phone)
        self.cell_phone = validate_phone(cell_phone)

    def __str__(self):
        return f"{self.surname}; {self.name}; {self.patronymic}; {self.organization}; {self.work_phone}; {self.cell_phone}"

    def edit(self, **kwargs):
        """
        Редактирование записи.
        :param kwargs: Словарь с новыми значениями атрибутов
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


