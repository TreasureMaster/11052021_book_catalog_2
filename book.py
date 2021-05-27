"""Implements the Book class containing the title, author, and page count."""
# Create your Book class in this file


class Book:
    """Implements the Book class."""

    def __init__(self, title='', author='', pages=0, is_completed=False):
        self.title = title
        self.author = author
        self.number_of_pages = int(pages)
        if isinstance(is_completed, bool):
            self.is_completed = is_completed
        elif is_completed in {'r', 'c'}:
            self.is_completed = True if is_completed == 'c' else False
        else:
            raise ValueError

    def __str__(self):
        return '{0} by {1}, {2} pages {3}'.format(
            self.title or '"Empty Book"',
            self.author or 'Unknown author',
            self.number_of_pages,
            '(completed)' if self.is_completed else '',
        )

    def str2csv(self):
        """Prepare book data for csv file."""
        return ','.join((
            self.title,
            self.author,
            str(self.number_of_pages),
            'c' if self.is_completed else 'r'
        ))

    def mark_required(self):
        """Mark the book as required."""
        self.is_completed = False

    def mark_completed(self):
        """Mark the book as completed."""
        self.is_completed = True

    def is_long(self):
        """Book length Test."""
        return self.number_of_pages > 500
