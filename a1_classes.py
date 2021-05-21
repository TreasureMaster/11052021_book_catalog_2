"""..."""
# Copy your first assignment to this file, then update it to use Book class
# Optionally, you may also use BookCollection class

from book import Book
from bookcollection import BookCollection

# Constants for application info
APP_NAME = 'Reading Tracker'
MY_NAME = 'Your Name'
VERSION = '2.0'
# Constants for work with files
FILENAME = 'books.csv'
# Constants for work with list of books
TITLE, AUTHOR, PAGES, MARK = range(4)
REQUIRED = 'r'
COMPLETED = 'c'
# List of quotes
QUOTES_LIST = [
    'So many books, so little time. Frank Zappa',
    'Books are a uniquely portable magic. Stephen King',
    'There is no friend as loyal as a book. Ernest Hemingway',
    'Sleep is good, he said, and books are better. George R. R. Martin',
    'I cannot live without books. Thomas Jefferson',
    'Books may well be the only true magic. Alice Hoffman',
    'Books are the mirrors of the soul. Virginia Woolf',
    'We live for books. Umberto Eco',
    'A book must be the axe for the frozen sea within us. Franz Kafka',
    'You cannot open a book without learning something. Confucius',
    'I just knew there were stories I wanted to tell. Octavia E. Butler'
]


# ---------------------------------- Menu ---------------------------------- #
def help_menu():
    """Help menu for control commands."""
    print(
        """Menu:
L - List all books
A - Add new book
M - Mark a book as completed
Q - Quit""")


# ----------------------------- for Add command ---------------------------- #
def get_added_book():
    """Add command implementation."""
    # Create a new book and add it to the list of books
    book = [
        add_string('title'),
        add_string('author'),
        add_number('pages'),
        REQUIRED
    ]
    print('{0}, ({1} pages) added to {2}'.format(
        book[TITLE],
        book[PAGES],
        APP_NAME
    ))
    return book


def add_string(name):
    """Add text entry."""
    # Add string entry and check its validity
    is_valid_input = False
    # PyCharm requirement
    entry = ''
    while not is_valid_input:
        try:
            entry = input('{}: '.format(name.capitalize()))
            if not entry:
                raise ValueError('Input can not be blank')
            else:
                is_valid_input = True
        except ValueError as exc:
            print(exc)
    return entry


def add_number(name='>>>'):
    """Add numeric entry."""
    if name != '>>>':
        name = name.capitalize() + ':'
    # Add numeric entry and check its validity
    is_valid_input = False
    # PyCharm requirement
    entry = ''
    while not is_valid_input:
        try:
            entry = input('{} '.format(name))
            try:
                # Пробуем преобразовать в int
                number = int(entry)
            except ValueError:
                raise ValueError('Invalid input; enter a valid number')
            if number <= 0:
                raise ValueError('Number must be > 0')
            else:
                is_valid_input = True
        except ValueError as exc:
            print(exc)
    return entry


# ---------------------------- for Mark command ---------------------------- #
def mark_book(books):
    """Mark command implementation."""
    is_input_required = is_required(books)
    # Header output if required books are available
    if is_input_required:
        print(books)
        print('Enter the number of a book to mark as completed')
    # Enter the number of the completed book
    while is_input_required:
        position = int(add_number()) - 1
        if position > len(books)-1:
            print('Invalid book number')
        elif books[position].is_completed:
            print('That book is already completed')
            break
        else:
            books[position].mark_completed()
            print('{0} by {1} completed!'.format(
                books[position].title,
                books[position].author
            ))
            break
    else:
        print('No required books')


def is_required(books):
    """Detects the presence of the required books"""
    required = False
    for book in books:
        # Search books marked REQUIRED
        if not book.is_completed:
            required = True
            break
    return required


# ------------------------------ for Challenge ----------------------------- #
def quotation():
    """Get some quotes from the list randomly."""
    import random
    return random.choice(QUOTES_LIST)


# -------------------------------- Main func ------------------------------- #
def main():
    """The main block of the program.

    The function implements program control,
    selection of control commands,
    loading and saving the list of books.
    """
    # Header output
    print('{0} {1} - by {2}'.format(APP_NAME, VERSION, MY_NAME))
    # Creating a collection of books
    books = BookCollection()
    # Formation of the list of books and display of the menu
    books.load_books(FILENAME, backup=True)
    print('{} books loaded'.format(len(books)))
    help_menu()

    # Loop control menu
    command = None
    while command != 'Q':
        command = input('>>> ').upper()
        if command == 'L':
            print(books)
        elif command == 'A':
            books.add_book(Book(*get_added_book()))
        elif command == 'M':
            mark_book(books)
        elif command == 'Q':
            continue
        else:
            print('Invalid menu choice')
        help_menu()

    # Record updated list of books
    books.save_books()
    print('{0} books saved to {1}'.format(len(books), FILENAME))
    print('{}'.format(quotation()))


if __name__ == '__main__':
    main()
