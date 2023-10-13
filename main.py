from classes import AddressBook, Record


def input_error(func):
    def inner(user_string):
        try:
            result = func(user_string)
            return result
        except KeyError:
            return 'Enter user name:'
        except ValueError:
            return 'Enter correct type:'
        except IndexError:
            return 'Please enter command, name, and phone:'
    return inner


COMMANDS_DESCRIPTION = {
    'add': 'Add a new contact',
    'add_phone': 'Add a new phone to an existing contact',
    'change': 'Change a contact\'s phone number',
    'phone': 'Get the phone number for a contact',
    'hello': 'Greet the bot',
    'show all': 'Show all contacts',
    'good bye': 'Exit the bot',
    'close': 'Exit the bot',
    'exit': 'Exit the bot',
    'help': 'Show available commands',
}


@input_error
def add_contact(data):
    name, phone = create_data(data)
    record_add = Record(name.lower())
    record_add.add_phone(phone)
    addressbook.add_record(record_add)
    return f'A new contact added successfully. {name} phone: {phone}'


@input_error
def add_new_phone(data):
    name, phone = create_data(data)
    record_add_phone = addressbook.data[name]
    record_add_phone.add_phone(phone)
    return f'A new phone: {phone}, has been added to contact name: {name}.'


@input_error
def change_contact(data):
    name, phone = create_data(data)
    new_phone = data[2]

    record_change = addressbook.data[name]
    if record_change.change_contact(old_phone=phone, new_phone=new_phone) is True:
        return f'A contact name: {name} number: {phone}, has been changed to {new_phone}.'
    else:
        return 'The phone number not exist'


@input_error
def get_number(name_contact):
    name = name_contact[0]
    if name in addressbook.data:
        record = addressbook.data[name]
        phones = ', '.join([phone.value for phone in record.phones])
        return f"Name: {record.name.value}, Phones: {phones}"
    else:
        return f"Contact with name '{name}' not found in the address book."


@input_error
def quit_func(quit_command):
    return f'Thank you for using our BOT!!'


@input_error
def hello_func(hello_command):
    return f"Hello! How can I help you?"


@input_error
def show_all_func(show_all_command):
    result = 'All contacts:\n'
    for name, record in addressbook.data.items():
        phones = ', '.join([phone.value for phone in record.phones])
        result += f"Name: {name}, Phone: {phones}\n"
    return result


@input_error
def help_func(help_command):
    commands_list = "\n".join(
        [f"{cmd}: {description}" for cmd, description in COMMANDS_DESCRIPTION.items()])
    return f"Available commands:\n{commands_list}"


@input_error
def delete_func(data):
    name, phone = create_data(data)
    record_delete = addressbook.data[name]

    if record_delete.delete_phone(phone) is True:
        return f'Contact name: {name} phone: {phone}, has been deleted.'

    else:
        return 'The phone number does not exist'


def create_data(data):
    name = data[0]
    phone = data[1]
    if name.isnumeric():
        raise ValueError('Wrong name.')
    if not phone.isnumeric():
        raise ValueError('Wrong phone.')
    return name, phone


def main():

    COMMANDS = {
        'add': add_contact,
        'add_phone': add_new_phone,
        'change': change_contact,
        'phone': get_number,
        'hello': hello_func,
        'show all': show_all_func,
        'good bye': quit_func,
        'close': quit_func,
        'exit': quit_func,
        'help': help_func,
    }

    print('Welcome to BOT >>>')

    while True:
        user_input = input('Enter a command: ').lower()

        if user_input == '.':
            break

        if user_input.split()[0] in COMMANDS:
            command = user_input.split()[0]
            arguments = user_input.split()[1:]
            result = COMMANDS[command](arguments)
            if result:
                print(result)

        elif user_input in COMMANDS:
            result = COMMANDS[user_input](user_input)
            if result:
                print(result)

        else:
            print(f"Incorrect input '{user_input}', please, try again:")


if __name__ == "__main__":
    addressbook = AddressBook()
    main()
