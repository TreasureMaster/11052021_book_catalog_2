"""..."""
# Copy your first assignment to this file, then update it to use Book class
# Optionally, you may also use BookCollection class

from book import Book
from bookcollection import BookCollection

# Constants for application info
APP_NAME = 'Reading Tracker'
MY_NAME = 'Your Name'
VERSION = '1.0'
# Constants for work with files
FILENAME = 'books.csv'
BACKUP_POSTFIX = '_backup'
# Constants for work with list of books
TITLE, AUTHOR, PAGES, MARK = range(4)
REQUIRED = 'r'
COMPLETED = 'c'
# Last position in list
LAST = -1
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


# ---------------------------- for List command ---------------------------- #
def listing_books(books):
    """List command implementation."""
    # Calculate lengths for aligning strings
    max_title = max_string_length(books, TITLE)
    max_author = max_string_length(books, AUTHOR)
    max_pages = max_string_length(books, PAGES)
    books.sort(key=how_sort)
    for num, book in enumerate(books, start=1):
        # Displaying a list of books
        print('{0}{1}. {2:<{5}} by {3:<{6}}  {4:>{7}} pages'.format(
            # REQUIRED or COMPLETED label
            '*' if book[MARK] == REQUIRED else ' ',
            # Book number in the list
            num,
            # Book data
            book[TITLE],
            book[AUTHOR],
            book[PAGES],
            # Lengths for aligning strings
            max_title,
            max_author,
            max_pages
        ))
    book_nums, page_nums = get_required_pages(books)
    if book_nums:
        print('You need to read {0} pages in {1} books.'.format(
            page_nums,
            book_nums
        ))
    else:
        print('No books left to read. Why not add a new book?')


def get_required_pages(books):
    """Get the required number of books and pages"""
    # Total number of books to be read
    book_nums = 0
    # Total number of pages to read
    page_nums = 0
    for book in books:
        # Accounting for books that you need to read
        if book[MARK] == REQUIRED:
            book_nums += 1
            page_nums += int(book[PAGES])
    return book_nums, page_nums


def max_string_length(books, pos):
    """Calculates the maximum length of string to align."""
    length = 0
    for book in books:
        ln = len(book[pos])
        if ln > length:
            length = ln
    return length


def how_sort(item):
    """Sorting book list template."""
    return item[AUTHOR], item[TITLE]


# ----------------------------- for Add command ---------------------------- #
def add_book(books):
    """Add command implementation."""
    # Create a new book and add it to the list of books
    books.append([
        add_string('title'),
        add_string('author'),
        add_number('pages'),
        REQUIRED
    ])
    print('{0}, ({1} pages) added to {2}'.format(
        books[LAST][TITLE],
        books[LAST][PAGES],
        APP_NAME
    ))
    return books


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
        listing_books(books)
        print('Enter the number of a book to mark as completed')
    # Enter the number of the completed book
    while is_input_required:
        position = int(add_number()) - 1
        if position > len(books)-1:
            print('Invalid book number')
        elif books[position][MARK] == COMPLETED:
            print('That book is already completed')
            break
        else:
            books[position][MARK] = COMPLETED
            print('{0} by {1} completed!'.format(
                books[position][TITLE],
                books[position][AUTHOR]
            ))
            break
    else:
        print('No required books')


def is_required(books):
    """Detects the presence of the required books"""
    required = False
    for book in books:
        # Search books marked REQUIRED
        if book[MARK] == REQUIRED:
            required = True
            break
    return required


# ------------------------- for Save/Load filename ------------------------- #
def read_list():
    """Read csv file and creates list of books.
    Saves old data to backup file."""
    book_file = open(FILENAME, 'r', encoding='utf-8')

    # Prepare filename for saving the previous list
    backup_name = FILENAME.rsplit('.', maxsplit=1)
    if len(backup_name) == 1:
        backup_name = backup_name[0] + BACKUP_POSTFIX
    else:
        backup_name = backup_name[0] + BACKUP_POSTFIX + '.' + backup_name[1]
    backup = open(backup_name, 'w', encoding='utf-8')

    # Read list of books and save old info in backup file
    books = []
    for line in book_file.readlines():
        backup.write(line)
        books.append(line.rstrip().split(','))
    book_file.close()
    backup.close()
    return books


def write_list(books):
    """Save updated list of books."""
    book_file = open(FILENAME, 'w', encoding='utf-8')
    for line in books:
        line = ','.join(line)
        book_file.write(line + '\n')
    book_file.close()


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
    books.load_books('books.csv')
    print('{} books loaded'.format(len(books)))
    help_menu()

    # Loop control menu
    while True:
        command = input('>>> ').upper()
        if command == 'L':
            listing_books(books)
        elif command == 'A':
            books = add_book(books)
        elif command == 'M':
            mark_book(books)
        elif command == 'Q':
            break
        else:
            print('Invalid menu choice')
        help_menu()

    # Record updated list of books
    # write_list(books)
    # print('{0} books saved to {1}'.format(len(books), FILENAME))
    # print('{}'.format(quotation()))


if __name__ == '__main__':
    main()
