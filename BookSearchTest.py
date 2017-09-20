import unittest
from BookSearch import *

class BookSearchTest(unittest.TestCase):

    test_json_path = 'json/bookdata.json'
    test_book_search = BookSearch(test_json_path)

    def test_book_search_loading(self):
        """
        Test that the creation, and subsequent loading, of a new BookSearch with
        a provided path will contain books.
        """
        # Expect the instantiated shared instance of BookSearch is not None.
        assert self.test_book_search._books is not None

        # Count the book keys available, should match the number provided in
        # JSON. In this case, 9.
        book_keys = self.test_book_search._books.keys()
        assert len(book_keys) is 9

    def test_book_search_find_books_with_sandwich(self):
        """
        Test that the BookSearch will find a common word, Sandwich.
        """
        query = 'sandwich'
        found_books = self.test_book_search.find_books_with(query)
        assert len(found_books) is 9

    def test_book_search_find_books_with_oberons(self):
        """
        Test that the BookSearch will find an uncommon word that is often
        written with punctuation, oberons (Oberon's as it usually appears in
        text).
        """
        query = "Oberon's"
        found_books = self.test_book_search.find_books_with(query)
        assert len(found_books) is 2

        # Now we try with the same word with out punctuation or an uppercase
        # letter
        query = "oberons"
        found_books = self.test_book_search.find_books_with(query)
        assert len(found_books) is 2

if __name__ == '__main__':
    unittest.main()
