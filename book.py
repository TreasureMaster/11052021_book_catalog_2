"""Implements the Book class containing the title, author, and page count."""
# Create your Book class in this file

from peewee import *


db = SqliteDatabase('books.db3')

class Book(Model):
    """Implements the Book class."""
    title = CharField()
    author = CharField()
    number_of_pages = IntegerField()
    is_completed = BooleanField(default=False)

    class Meta:
        database = db

# class Book:

    # def __init__(self, title='', author='', pages=0, is_completed=False):
    #     self.title = title
    #     self.author = author
    #     self.number_of_pages = int(pages)
    #     if isinstance(is_completed, bool):
    #         self.is_completed = is_completed
    #     elif is_completed in {'r', 'c'}:
    #         self.is_completed = True if is_completed == 'c' else False
    #     else:
    #         raise ValueError

    def __str__(self):
        return '{0}, автор {1}, {2} стр. {3}'.format(
            self.title or '"Неизвестная книга"',
            self.author or 'Неизвестный автор',
            self.number_of_pages,
            '(прочитана)' if self.is_completed else '',
        )

    # def str2csv(self):
    #     """Prepare book data for csv file."""
    #     # NOTE устарел, csv не будет использоваться
    #     return ','.join((
    #         self.title,
    #         self.author,
    #         str(self.number_of_pages),
    #         'c' if self.is_completed else 'r'
    #     ))

    def mark_required(self):
        """Mark the book as required."""
        self.is_completed = False
        self.save()

    def mark_completed(self):
        """Mark the book as completed."""
        self.is_completed = True
        self.save()

    def is_long(self):
        """Book length Test."""
        return self.number_of_pages > 500
