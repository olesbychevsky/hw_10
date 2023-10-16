from collections import UserDict

class Field:
    def __init__(self, name):
        self.value = name

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, number):
        if not self.is_valid_phone(number):
            raise ValueError('Phone number must be a 10-digit number.')
        super().__init__(number)

    @staticmethod
    def is_valid_phone(number):
        return len(number) == 10 and number.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if self.is_valid_phone(phone):
            self.phones.append(phone)
        else:
            raise ValueError('Phone number must be a 10-digit number.')

    @staticmethod
    def is_valid_phone(number):
        return len(number) == 10 and number.isdigit()

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
            return f'Phone {old_phone} has been updated to {new_phone} in the record: {self.name.value}'
        else:
            raise ValueError(f'Phone {old_phone} not found in the record.')




    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if isinstance(phone, Phone) and phone.value == phone_to_find:
                return phone
        return None

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError('Phone not found in the record.')

def input_error(func):
    def inner(user_string):
        try:
            result = func(user_string)
            return result
        except KeyError:
            return 'Enter user name:'
        except ValueError as e:
            return str(e)
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

def create_data(data):
    if len(data) != 2:
        raise IndexError('Please enter command, name, and phone.')
    name = Name(data[0])
    phone = Phone(data[1])
    return name, phone

@input_error
def add_contact(data):
    name, phone = create_data(data)
    record_add = Record(name)
    record_add.add_phone(phone)
    addressbook.add_record(record_add)
    return f'A new contact added successfully. {name.value} phone: {phone.value}'

@input_error
def add_new_phone(data):
    name, phone = create_data(data)
    record_add_phone = addressbook.data.get(name.value)
    if record_add_phone:
        record_add_phone.add_phone(phone)
        return f'A new phone: {phone.value}, has been added to contact name: {name.value}.'
    else:
        return f'Contact with name "{name.value}" not found in the address book.'

@input_error
def change_contact(data):
    name, phone = create_data(data)
    new_phone = Phone(data[2])

    record_change = addressbook.data.get(name.value)
    if record_change:
        try:
            return record_change.edit_phone(phone.value, new_phone.value)
        except ValueError as e:
            return str(e)
    else:
        return f'Contact with name "{name.value}" not found in the address book.'

@input_error
def get_number(name_contact):
    name = name_contact[0]
    record = addressbook.data.get(name.value)
    if record:
        phones = ', '.join([phone.value for phone in record.phones])
        return f"Name: {name.value}, Phones: {phones}"
    else:
        return f'Contact with name "{name.value}" not found in the address book.'

@input_error
def show_all_func(show_all_command):
    result = 'All contacts:\n'
    for name, record in addressbook.data.items():
        phones = ', '.join([phone.value for phone in record.phones])
        result += f"Name: {name}, Phone: {phones}\n"
    return result

@input_error
def quit_func(quit_command):
    return 'Thank you for using our BOT!'

@input_error
def hello_func(hello_command):
    return "Hello! How can I help you?"

@input_error
def help_func(help_command):
    commands_list = "\n".join(
        [f"{cmd}: {description}" for cmd, description in COMMANDS_DESCRIPTION.items()])
    return f"Available commands:\n{commands_list}"

@input_error
def find_contact(data):
    name = data[0]
    return addressbook.find(name)

@input_error
def delete_contact(data):
    name = data[0]
    if name.value in addressbook.data:
        del addressbook.data[name.value]
        return f'Contact with name "{name.value}" has been deleted.'
    else:
        return f'Contact with name "{name.value}" not found in the address book.'

def main():
    global addressbook
    addressbook = AddressBook()

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
        'delete': delete_contact,
        'find': find_contact,
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
        else:
            print(f"Incorrect input '{user_input}', please, try again:")

if __name__ == "__main__":
    main()
