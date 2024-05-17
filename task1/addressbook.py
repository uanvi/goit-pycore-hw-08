import datetime
from collections import UserDict
from errhandler import InvalidPhoneError, InvalidBirthdayError

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise InvalidPhoneError()
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

class Birthday:
    def __init__(self, value):
        try:
            # date format validation
            self.date = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise InvalidBirthdayError()

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = set()
        self.birthday = None

    def add_phone(self, phone):
        self.phones.add(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = birthday

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = Phone(new_phone)
                break

    def find_phone(self, phone):
        return phone in [p.value for p in self.phones]

    def __str__(self):
        phone_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phone_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.datetime.today()

        for record in self.values():
            if record.birthday:
                birthday = record.birthday.date
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta = birthday_this_year - today
                if 0 <= delta.days <= 7:  # Include birthdays occurring in the next 7 days
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() >= 5:  # If birthday falls on a weekend
                        # Move congratulation date to the next Monday
                        congratulation_date += datetime.timedelta(days=7 - congratulation_date.weekday())
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})

        return upcoming_birthdays
