"""(Incomplete) Tests for Book class."""
from book import Book


def run_tests():
    """Test Book class."""

    # Test empty book (defaults)
    print("Test empty book:")
    default_book = Book()
    print(default_book)
    assert default_book.title == ""
    assert default_book.author == ""
    assert default_book.number_of_pages == 0
    assert not default_book.is_completed

    # Test initial-value book
    print("Test initial-value book:")
    new_book = Book("Fish Fingers", "Dory", 501, True)
    # TODO: Write tests to show this initialisation works

    # Test mark_required()
    # TODO: Write tests to show the mark_required() method works

    # Test is_long()
    # TODO: Write tests to show the is_long() method works

    # TODO: Add more tests, as appropriate


run_tests()
