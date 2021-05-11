"""..."""
from book import Book

# Create your BookCollection class in this file


class BookCollection:
    """Implements the BookCollection class."""
    # BACKUP_POSTFIX = '_backup'
    TITLE = 'title'
    AUTHOR = 'author'
    PAGES = 'number_of_pages'

    def __init__(self):
        self.books = []

    def __str__(self):
        """List command implementation."""
        # books.sort(key=how_sort)
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
        string = string.rstrip()
        if string:
            return string
        else:
            return 'Collection of books is empty.'

    def max_string_length(self, attr):
        """Calculates the maximum length of string to align."""
        length = 0
        for book in self.books:
            ln = len(getattr(book, attr))
            if ln > length:
                length = ln
        return length

    def load_books(self, filename=''):
        """Read csv file and creates list of books."""
        book_file = open(filename, 'r', encoding='utf-8')
        for line in book_file.readlines():
            self.books.append(Book(*line.rstrip().split(',')))
        book_file.close()

    def save_backup(self):
        """Saves old data to backup file."""
        raise NotImplementedError


if __name__ == '__main__':
    col = BookCollection()
    col.load_books('books.csv')
    for book in col.books:
        print(book)
    print(col.max_string_length(col.PAGES))
    # print(col.max_string_length(col.AUTHOR))
    # print(col.max_string_length(col.TITLE))
    print(col)