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
    print('--- Passed.')

    # Test initial-value book
    print("Test initial-value book:")
    new_book = Book("Fish Fingers", "Dory", 501, True)
    # Write tests to show this initialisation works
    print(new_book)
    assert new_book.title == "Fish Fingers"
    assert new_book.author == "Dory"
    assert new_book.number_of_pages == 501
    assert new_book.is_completed
    assert str(new_book) == 'Fish Fingers by Dory, 501 pages (completed)'
    print('--- Passed.')

    # Test mark_required()
    print("Book marking Test:")
    # Write tests to show the mark_required() method works
    new_book.mark_required()
    assert not new_book.is_completed
    new_book.mark_completed()
    assert new_book.is_completed
    print('--- Passed.')

    # Test is_long()
    print("Book length Test:")
    # Write tests to show the is_long() method works
    assert not default_book.is_long()
    assert new_book.is_long()
    print('--- Passed.')

    # TODO: Add more tests, as appropriate
    # Test for csv line
    print("Get csv line Test:")
    assert new_book.str2csv() == 'Fish Fingers,Dory,501,c'
    other_book = Book("The 360 Degree Leader", "John Maxwell", 369, False)
    assert other_book.str2csv() == 'The 360 Degree Leader,John Maxwell,369,r'
    print('--- Passed.')


run_tests()
