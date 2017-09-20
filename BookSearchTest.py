import unittest
from BookSearch import *

class BookSearchTest(unittest.TestCase):

    test_json_path = 'json/bookdata.json'

    def test_book_search_loading(self):
        """
        Test that the creation, and subsequent loading, of a new BookSearch with
        a provided path will contain books.
        """
        test_book_search = BookSearch(self.test_json_path)
        assert test_book_search._books is not None

if __name__ == '__main__':
    unittest.main()
