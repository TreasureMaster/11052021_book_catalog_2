"""(Incomplete) Tests for BookCollection class."""
from bookcollection import BookCollection
from book import Book


def run_tests():
    """Test BookCollection class."""

    # Test empty BookCollection (defaults)
    print("Test empty BookCollection:")
    book_collection = BookCollection()
    print(book_collection)
    assert not book_collection.books  # PEP 8 suggests not using len() to test for empty lists
    print('--- Passed.')

    # Test loading books
    print("Test loading books:")
    book_collection.load_books('books.csv')
    print(book_collection)
    assert book_collection.books  # assuming CSV file is non-empty, length should be non-zero
    print('--- Passed.')

    # Test adding a new Book with values
    print("Test adding new book:")
    book_collection.add_book(Book("War and Peace", "William Shakespeare", 999, False))
    print(book_collection)
    print('--- Passed.')

    # Test sorting books
    print("Test sorting - author:")
    book_collection.sort("author")
    print(book_collection)
    print('--- Passed.')

    # Add more sorting tests
    print("Test sorting - title:")
    book_collection.sort("title")
    print(book_collection)
    print('--- Passed.')

    print("Test sorting - number_of_pages:")
    book_collection.sort("number_of_pages")
    print(book_collection)
    print('--- Passed.')

    print("Test sorting - pages:")
    book_collection.sort("pages")
    print(book_collection)
    print('--- Passed.')

    # Test get_required_pages() and get_required_books()
    print("Test get_required_pages() and get_required_books():")
    new_book_collection = BookCollection()
    # Add required book
    new_book_collection.add_book(Book("War and Peace", "William Shakespeare", 999, False))
    assert new_book_collection.get_required_pages() == 999
    assert new_book_collection.get_required_books() == 1
    # Add required book
    new_book_collection.add_book(Book("The 360 Degree Leader", "John Maxwell", 369, False))
    assert new_book_collection.get_required_pages() == 1368
    assert new_book_collection.get_required_books() == 2
    # Add completed book
    new_book_collection.add_book(Book("In Search of Lost Time", "Marcel Proust", 93, True))
    assert new_book_collection.get_required_pages() == 1368
    assert new_book_collection.get_required_books() == 2
    print('--- Passed.')

    # Test saving books (check CSV file manually to see results)
    print("Test saving books:")
    # 5 books sorted by pages
    book_collection.save_books('collection.csv')
    # 3 books
    new_book_collection.save_books('new_books.csv')
    print('--- Passed.')

    # TODO: Add more tests, as appropriate
    # Test max_string_length()
    print("Test max_string_length():")
    assert new_book_collection.max_string_length(BookCollection.TITLE) == 22
    assert new_book_collection.max_string_length(BookCollection.AUTHOR) == 19
    assert new_book_collection.max_string_length(BookCollection.PAGES) == 3
    print('--- Passed.')

    # Test: books collection length get
    print("Test collection length:")
    assert len(new_book_collection) == 3
    assert len(book_collection) == 5
    print('--- Passed.')

    # Test: backup filename get
    print("Test backup filename getting:")
    assert new_book_collection.get_backup_name('collection.csv') == 'collection_backup.csv'
    assert new_book_collection.get_backup_name('books') == 'books_backup'
    print('--- Passed.')

    # Test: Getting books from the collection
    print('Test book get as list:')
    assert str(new_book_collection[0]) == '*William Shakespeare. War and Peace, pp. 999'
    assert str(new_book_collection[2]) == ' Marcel Proust. In Search of Lost Time, pp. 93'
    print('--- Passed.')


run_tests()
