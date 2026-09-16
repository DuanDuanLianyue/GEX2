##Import the necessary module
import json
from pathlib import Path


## This function should load the library data from a JSON file and return it as a suitable Python data structure.
def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)



## This function should save the library data to a JSON file.
## This function does not need to return anything, but it should ensure that the data is saved correctly to the specified file.
def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    



## This function should find a book by its title, author, or ID.
## If the book is found, it should return the book ID.
## If the book is not found, it should return None.
def find_book(books, search_text):
    normalized_search = str(search_text).strip().casefold()

    if not normalized_search:
        return None

    for book_id, book in books.items():
        searchable_values = (
            str(book_id),
            str(book.get("title", "")),
            str(book.get("author", ""))
        )

        if any(
            value.strip().casefold() == normalized_search
            for value in searchable_values
        ):
            return book_id

    return None



## This function should display the list of books in a user-friendly format.
## It should show the book ID, title, category, and availability status (available or on loan).
## If the book is available, it should display "AVAILABLE", and if it is on loan, it should display "ON LOAN".
## The function should not return anything, but it should print the information to the console.
## The heading for this display should be "BOOK CATALOGUE".
def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)

    for book_id, book in books.items():
        status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
        print(
            f"{book_id} | {book.get('title', '')} | "
            f"{book.get('category', '')} | {status}"
        )


## This function should display the list of current loans in a user-friendly format.
## It should show the book ID, title, and the name of the borrower.
## The heading for this display should be "CURRENT LOANS".
## The function should not return anything, but it should print the information to the console.
def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)

    for loan in loans:
        book_id = loan.get("book_id", "")
        book = books.get(book_id, {})
        title = book.get("title", "Unknown title")
        borrower = loan.get("borrower", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")


## This function should calculate and return the library statistics
## The statsitics should include the total number of books, the number of available books, and the number of borrowed books.
## The function should return these three values in the order: total, available, borrowed. Use a suitable data structure to return these values, such as a tuple or a dictionary.

def library_statistics(books):
    total = len(books)
    available = sum(
        1
        for book in books.values()
        if book.get("available", False)
    )
    borrowed = total - available

    return total, available, borrowed


## This function should display the library statistics in a user-friendly format.
## It should first load the library data from a JSON file, 
## Then calculate the statistics, and finally print the information to the console.
## The heading for this display should be "LIBRARY STATISTICS".
## It should print the total number of books, the number of available books, and the number of borrowed books.
## The function should not return anything, but it should print the information to the console.
def main():
    filename = Path(__file__).with_name("library.json")
    data = load_library(filename)

    library = data.get("library", {})
    categories = data.get("categories", [])
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library.get('name', '')}")
    print(f"Branch: {library.get('branch', '')}")
    print(f"Year: {library.get('year', '')}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()
    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)
    print("LIBRARY STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


## Following is how the Admin interface should look like when the program is run. 
# The actual output may vary based on the library data and the current state of loans.

""" 
LIBRARY ADMINISTRATION
============================================================
Library: 
Branch: 
Year: 
Categories: 

BOOK CATALOGUE
------------------------------------------------------------
ID1 | Title1 | Category | Availability
ID2 | Title2 | Category | Availability
...
...
...
IDN | TitleN | Category | Availability


CURRENT LOANS
------------------------------------------------------------
ID1 | Title1 | Borrower: Borrower1
ID2 | Title2 | Borrower: Borrower2
...
...
...
IDN | TitleN | Borrower: BorrowerN

STATISTICS
------------------------------------------------------------
Total books: XX
Available: XX
Borrowed: XX
"""


if __name__ == "__main__":
    main()
