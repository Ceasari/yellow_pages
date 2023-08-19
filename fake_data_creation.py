from faker import Faker
from records import Record
from directory import Directory

fake = Faker("ru_RU")

def generate_fake_record():
    surname = fake.last_name()
    name = fake.first_name()
    patronymic = fake.middle_name()
    organization = fake.company()
    work_phone = fake.phone_number()
    cell_phone = fake.phone_number()
    return Record(surname, name, patronymic, organization, work_phone, cell_phone)


def fill_directory_with_fake_records(directory, num_records):
    for _ in range(num_records):
        fake_record = generate_fake_record()
        directory.add_record(fake_record)
    directory.save_to_file()


if __name__ == "__main__":
    num_fake_records = 3000
    directory = Directory.load_from_file()
    fill_directory_with_fake_records(directory, num_fake_records)
    print(f"Добавлено {num_fake_records} фэйковых контактов в справочник.")
