from errhandler import input_error
from addressbook import AddressBook, Birthday, Record
from serialization import save_data, load_data


def parse_input(user_input):
    """Parse bot command and arguments
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error(2)
def add_contact(args, contacts):
    """Bot add command implementation
    """
    name, phone = args
    record = contacts.find(name)
    if record:
        record.add_phone(phone)
        return "Added new phone to existing contact"
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Contact added."

@input_error(3)
def change_contact(args, contacts):
    """Bot change command implementation
    """
    name, oldphone, phone = args
    record = contacts.find(name)
    if record is None:
        return f"There is no contact with the name '{name}'"

    record.edit_phone(oldphone, phone)
    return f"For contact '{name}' phone changed."

@input_error(0)
def get_all_contacts(args, contacts):
    """Bot all command implementation
    """
    return "\n".join([str(record.name) for record in contacts.data.values()])

@input_error(1)
def get_phone_by_user(args, contacts):
    """Bot phone command implementation"""
    name = args[0]
    record = contacts.find(name)
    if record is None:
        return f"There is no contact with the name '{name}'"

    return record

@input_error(2)
def add_birthday(args, contacts):
    """Bot add-birthday command implementation
    """
    name, birthday = args
    record = contacts.find(name)
    if record is None:
        return f"There is no contact with the name '{name}'"

    record.add_birthday(Birthday(birthday))
    return "Birthday added."

@input_error(1)
def show_birthday(args, book):
    """Bot show-birthday command implementation
    """
    name = args[0]
    if name not in book.data:
        return f"There is no contact with the name '{name}'"
    record = book.find(name)
    if record.birthday:
        return f"The birthday of {name} is {record.birthday}"
    else:
        return f"{name} does not have a birthday set."

@input_error(0)
def birthdays(args, book):
    """Bot birthdays command implementation
    """
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "There are no upcoming birthdays next week."
    else:
        return upcoming_birthdays


def main():
    book = load_data()
    try:
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Goodbye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "all":
                print(get_all_contacts(args, book))
            elif command == "phone":
                print(get_phone_by_user(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        save_data(book)

if __name__ == "__main__":
    main()
