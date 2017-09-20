import json
import re

class BookSearch(object):
    def __init__(self, path):
        self._books = self._load_books(path)
        self._books_by_word = self._process_books()

    def _load_books(self, path):
        """
        Loads book JSON data.
        """
        with open(path) as json_file:
            return json.load(json_file)

    def _process_books(self):
        """
        Generates a Dictionary of book briefs (a simplified string
        representation of a book) keyed to every word from every book
        provided.

        1. Creates the Dictionary
        2. Cycles through each book
        3. Generates a complete list of the unique words in the book
        4. Cycles through each word
        5. Saves book brief to a Set under that word
        """
        keyed_books = {}
        for book_id in self._books.keys():
            book = self._books.get(book_id)
            # Here we create a record of the book to save in our records.
            # Consists of only the book ID and Title.
            book_brief = "Book ID: " + book_id + " | Title: " + book["title"]

            # Get a list of all the words in the title and description
            words = self._get_all_book_words(book)
            for word in words:
                if keyed_books.get(word) != None:
                    keyed_books[word].add(book_brief)
                else:
                    keyed_books[word] = {book_brief}
        return keyed_books

    def _get_all_book_words(self, book):
        """
        For a given book, creates and returns a single set of words found in a
        book's title and description.
        """
        book_words = self._strip_and_list_words(book.get('title'))
        book_words.update(self._strip_and_list_words(book.get('description')))
        return book_words

    def _strip_and_list_words(self, word_string):
        """
        For a given string, strips all non-alphanumeric characters, converts to
        lowercase, and splits by spaces into a set of all the words.
        """
        stripped_words = re.sub('[^a-zA-Z ]', '', word_string).lower()
        words_list = stripped_words.split()
        return set(words_list)

    def find_books_with(self, query_words):
        """
        For a given query string, all query words are checked as keys against
        the collection of books keyed by word. All books found are returned as a
        set.
        """
        cleaned_query_words = self._strip_and_list_words(query_words)

        # Cycle through all the query words and build up a set of books with one
        # or many matching words.
        found_books = set()
        for query_word in cleaned_query_words:
            found_books.update(self._books_by_word.get(query_word))

        return found_books

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Find books for query words.')
    parser.add_argument('strings', metavar='N', type=str, nargs='+',
                   help='a word to search for in each book in the library.')
    args = parser.parse_args()

    # Instantiate a new instance of BookSearch, using default json data.
    path = 'json/bookdata.json'
    current_book_search = BookSearch(path)

    # Find some books!
    found_books = current_book_search.find_books_with(' '.join(args.strings))

    # Print what books were found, if any.
    if found_books:
        for book in found_books:
            print(book)
    else:
        print("No books found.")
