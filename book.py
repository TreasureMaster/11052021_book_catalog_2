"""Implements the Book class containing the title, author, and page count."""
# Create your Book class in this file


class Book:
    """Implements the Book class."""

    def __init__(self, title='', author='', pages=0, is_comleted=False):
        self.title = title
        self.author = author
        self.number_of_pages = pages
        self.is_completed = is_comleted

    def __str__(self):
        return '{0}{1}. {2}, pp. {3}'.format(
            ' ' if self.is_completed else '*',
            self.author or 'Unknown author',
            self.title or '"Empty Book"',
            self.number_of_pages
        )
