import json
import re

class BookSearch(object):
    def __init__(self, path):
        self._books = self._load_books(path)
        self._books_by_word = self._process_books()

    def _load_books(self, path):
        # import ipdb; ipdb.set_trace()
        with open(path) as json_file:
            return json.load(json_file)

    def _process_books(self):
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
        book_words = self._strip_and_list_words(book.get('title'))
        book_words.update(self._strip_and_list_words(book.get('description')))
        return book_words

    def _strip_and_list_words(self, word_string):
        stripped_words = re.sub('[^a-zA-Z ]', '', word_string).lower()
        words_list = stripped_words.split()
        return set(words_list)

    def find_books_with(self, query_words):
        cleaned_query_words = self._strip_and_list_words(query_words)
        for query_word in cleaned_query_words:
            foundBooks = self._books_by_word.get(query_word)
            return foundBooks

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Find books for query words.')
    parser.add_argument('strings', metavar='N', type=str, nargs='+',
                   help='an integer for the accumulator')
    args = parser.parse_args()

    path = 'json/bookdata.json'
    current_book_search = BookSearch(path)

    # Create a set to save found books for queried words to reduce duplicates
    found_books = set()
    for queryWord in args.strings:
        found_new_books = current_book_search.find_books_with(queryWord)
        if found_new_books:
            found_books.update(found_new_books)

    # Print what books were found, if any.
    if found_books:
        for book in found_books:
            print(book)
    else:
        print("No books found.")
