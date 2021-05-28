"""..."""
import operator
from book import Book

# Create your BookCollection class in this file


class BookCollection:
    """Implements the BookCollection class."""
    BACKUP_POSTFIX = '_backup'
    TITLE = 'title'
    AUTHOR = 'author'
    PAGES = 'number_of_pages'

    def __init__(self):
        self.books = []
        self.filename = ''

    def __str__(self):
        """List command implementation."""
        string = ''
        for num, book in enumerate(self.books, start=1):
            # Displaying a list of books
            string += ('{0}{1}. {2:<{5}} by {3:<{6}}  {4:>{7}} page{8}\n'.format(
                # REQUIRED or COMPLETED label
                ' ' if book.is_completed else '*',
                # Book number in the list
                num,
                # Book data
                book.title,
                book.author,
                book.number_of_pages,
                # Lengths for aligning strings
                self.max_string_length(BookCollection.TITLE),
                self.max_string_length(BookCollection.AUTHOR),
                self.max_string_length(BookCollection.PAGES),
                '' if book.number_of_pages == 1 else 's'
            ))
        if string:
            required = ('You need to read {0} pages in {1} books.'.format(
                self.get_required_pages(),
                self.get_required_books()
            ))
            return string + required
        else:
            return 'Collection of books is empty.'

    def __len__(self):
        """Returns length of collection."""
        return len(self.books)

    def __getitem__(self, key):
        """Returns book from collection."""
        return self.books[key]

    def __iter__(self):
        """PyCharm requirements."""
        return iter(self.books)

    def max_string_length(self, attr):
        """Calculates the maximum length of string to align."""
        length = 0
        for book in self.books:
            ln = len(str(getattr(book, attr)))
            if ln > length:
                length = ln
        return length

    def load_books(self, filename='', backup=False):
        """Read csv file and creates list of books."""
        self.filename = filename
        book_file = open(filename, 'r', encoding='utf-8')
        for line in book_file.readlines():
            self.books.append(Book(*line.rstrip().split(',')))
        book_file.close()
        if backup:
            self.save_books(self.get_backup_name(filename))

    def save_books(self, filename=''):
        """Save csv file for list of books."""
        filename = filename or self.filename
        book_file = open(filename, 'w', encoding='utf-8')
        for book in self.books:
            print(book.str2csv(), file=book_file)
        book_file.close()

    def get_backup_name(self, filename=''):
        """Get backup filename."""
        backup_name = filename.rsplit('.', maxsplit=1)
        if len(backup_name) == 1:
            backup_name = backup_name[0] + BookCollection.BACKUP_POSTFIX
        else:
            backup_name = backup_name[0] + BookCollection.BACKUP_POSTFIX + '.' + backup_name[1]
        return backup_name

    def add_book(self, book):
        """Add book in collection."""
        self.books.append(book)

    def sort(self, by_sort='author'):
        """Sort books in collection by field."""
        by_sort = by_sort.lower()
        if by_sort == 'pages':
            by_sort = 'number_of_pages'
        if by_sort == 'completed':
            by_sort = 'is_completed'
        if by_sort == 'author' or by_sort == 'title':
            how_sort = lambda m: operator.attrgetter(by_sort)(m).lower()
        else:
            how_sort = operator.attrgetter(by_sort)
        self.books.sort(
            # key=(lambda m: operator.attrgetter(by_sort)(m).lower()) if by_sort != 'number_of_pages' else operator.attrgetter(by_sort),
            key=how_sort,
            reverse=(True if by_sort == 'is_completed' else False)
        )

    def get_required_pages(self):
        """Get the required number of pages."""
        # Total number of pages to read
        page_nums = 0
        for book in self.books:
            # Accounting for books that you need to read
            if not book.is_completed:
                page_nums += book.number_of_pages
        return page_nums

    def get_required_books(self):
        """Get the required number of books."""
        # Total number of pages to read
        book_nums = 0
        for book in self.books:
            # Accounting for books that you need to read
            if not book.is_completed:
                book_nums += 1
        return book_nums
