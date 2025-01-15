import os
import json
import re


class LibraryManager:
    def __init__(self, filename='library.txt'):
        self.filename = filename
        self.books = {}  # this is dictionary where keys are authors and values are lists of books
        self.borrowedBooks = set()
        self.availableBooks = set()
        self.loadBooks()

# load book library data from file if it exists
    def loadBooks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                # convert books dictionary keys to integers just in case
                self.books = {}
                for author, bookList in data.get("books", {}).items():
                    self.books[author] = [
                        {"index": int(book["index"]), "title": book["title"], "year": book["year"]}
                        for book in bookList
                    ]
                
                # convert borrowedBooks and availableBooks to integers
                borrowedBooks = data.get("borrowedBooks", [])
                self.borrowedBooks = set()
                for idx in borrowedBooks:
                    self.borrowedBooks.add(int(idx))

                availableBooks = data.get("availableBooks", [])
                self.availableBooks = set()
                for idx in availableBooks:
                    self.availableBooks.add(int(idx))

                # if both borrowedBooks and availableBooks are empty, set all books as available
                if not self.borrowedBooks and not self.availableBooks:
                    for authorBooks in self.books.values():
                        for book in authorBooks:
                            self.availableBooks.add(book["index"])
        else:
            self.books = {}
            self.borrowedBooks = set()
            self.availableBooks = set()

# save library data to file
    def saveBooks(self):
        data = {
            "books": self.books,
            "borrowedBooks": list(self.borrowedBooks),
            "availableBooks": list(self.availableBooks)
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file)

# add book to the library
    def addBooks(self, author, title, year):
        try:
            year = int(year)
            if year < 1000 or year > 9999:
                raise ValueError
        except ValueError:
            print("Invalid publication year. Please enter a valid year (e.g., 1996).")
            return

        index = len(self.availableBooks | self.borrowedBooks) + 1
        new_book = {
            "index": index,
            "title": title,
            "year": year
        }
        if author not in self.books:
            self.books[author] = []
        self.books[author].append(new_book)
        self.availableBooks.add(index)
        print(f"Book added with index {index}.")

# search books by author or title, supporting wildcard (*) searches for incomplete matches.
# wildcard '*' matches zero or more characters.
    def searchBooks(self, keyword):
        results = []
        keyword = keyword.lower()

        # check if wildcard is used
        if '*' in keyword:
            keyword = keyword.replace('*', '.*')  # replace * with regex equivalent
            pattern = re.compile(keyword)  # compile regex patern for wildcard matching
            for author, books in self.books.items():
                for book in books:
                    if pattern.search(author.lower()) or pattern.search(book["title"].lower()):
                        status = "(Borrowed)" if book["index"] in self.borrowedBooks else "(Available)"
                        results.append({"author": author, "book": book, "status": status})
        else:
            # do partial matching without wildcards
            for author, books in self.books.items():
                for book in books:
                    if keyword in author.lower() or keyword in book["title"].lower():
                        status = "(Borrowed)" if book["index"] in self.borrowedBooks else "(Available)"
                        results.append({"author": author, "book": book, "status": status})
        return results

# borrow a book if it is available
    def borrowBooks(self, index):
        if index in self.availableBooks:
            self.availableBooks.remove(index)
            self.borrowedBooks.add(index)
            print(f"Book with index {index} borrowed.")
        else:
            print(f"Book with index {index} is not available for borrowing.")

# return book
    def returnBooks(self, index):
        if index in self.borrowedBooks:
            self.borrowedBooks.remove(index)
            self.availableBooks.add(index)
            print(f"Book with index {index} returned.")
        else:
            print(f"Book with index {index} is not borrowed.")


# list all books and optionally show only available books
    def listBooks(self, show_all=True):
        """List all books, optionally showing only available books."""
        print("\nLibrary Books:")
        for author, books in self.books.items():
            for book in books:
                if book["index"] in self.borrowedBooks:
                    status = "\033[31m(Borrowed)\033[0m"  # Red for Borrowed
                else:
                    status = "\033[32m(Available)\033[0m"  # Green for Available

                if show_all or book["index"] in self.available_books:
                    print(f"Index: {book['index']}, {author}, {book['title']}, {book['year']} {status}")
        print()

    def saveAndExit(self):
        """Save data and exit."""
        self.saveBooks()
        print("Library data saved. Exiting...")

def main():
    manager = LibraryManager()

    while True:
        print("\n=== Library Manager ===")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. List All Books")
        print("6. List Available Books")
        print("7. Save and exit.")
        choice = input("\nPlease Choose: ").strip()

        if choice == '1':
            author = input("\nEnter author name: ")
            title = input("Enter book title: ")
            year = input("Enter publication year: ")
            manager.addBooks(author, title, year)
        elif choice == '2':
            keyword = input("\nEnter keyword to search (author/title or use * for wildcard): ")
            results = manager.searchBooks(keyword)
            if results:
                print("\nearch Results:\n")
                for result in results:
                    author = result["author"]
                    book = result["book"]
                    status = result["status"]
                    print(f"Index: {book['index']}, {author}, {book['title']}, {book['year']} {status}")
            else:
                print("No books found.")
        elif choice == '3':
            try:
                index = int(input("\nEnter book index to borrow: "))
                manager.borrowBooks(index)
            except ValueError:
                print("\nInvalid input. Please enter a valid index.")
        elif choice == '4':
            try:
                index = int(input("\nEnter book index to return: "))
                manager.returnBooks(index)
            except ValueError:
                print("\nInvalid input. Please enter a valid index.")
        elif choice == '5':
            manager.listBooks()
        elif choice == '6':
            manager.listBooks(show_all=False)
        elif choice == '7':
            manager.saveAndExit()
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()