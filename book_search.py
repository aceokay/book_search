import json
import re

class book_search(object):
    def __init__(self, path):
        self._books = self._loadBooks(path)
        self._books_by_word = self._processBooks()

    def _loadBooks(self, path):
        # import ipdb; ipdb.set_trace()
        with open(path) as json_file:
            return json.load(json_file)

    def _processBooks(self):
        keyed_books = {}
        for book_id in self._books.keys():
            book = self._books.get(book_id)
            # Here we create a record of the book to save in our records.
            # Consists of only the book ID and Title.
            book_brief = "Book ID: " + book_id + " | Title: " + book["title"]

            # Get a list of all the words in the title and description
            words = self._getAllBookWords(book)
            for word in words:
                if keyed_books.get(word) != None:
                    keyed_books[word].add(book_brief)
                else:
                    keyed_books[word] = {book_brief}
        return keyed_books

    def _getAllBookWords(self, book):
        book_words = self._stripAndListWords(book.get('title'))
        book_words.update(self._stripAndListWords(book.get('description')))
        return book_words

    def _stripAndListWords(self, word_string):
        stripped_words = re.sub('[^a-zA-Z ]', '', word_string).lower()
        words_list = stripped_words.split()
        return set(words_list)

    def findBooksWith(self, query_words):
        cleaned_query_words = self._stripAndListWords(query_words)
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
    current_book_search = book_search(path)

    # Create a set to save found books for queried words to reduce duplicates
    found_books = set()
    for queryWord in args.strings:
        found_new_books = current_book_search.findBooksWith(queryWord)
        if found_new_books:
            found_books.update(found_new_books)

    # Print what books were found, if any.
    if found_books:
        for book in found_books:
            print(book)
    else:
        print("No books found.")
