## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    find_book,
    load_library,
    save_library
)

from pathlib import Path



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    normalized_category = category.strip().casefold()

    if not normalized_category:
        return []

    return [
        book_id
        for book_id, book in books.items()
        if str(book.get("category", "")).strip().casefold()
        == normalized_category
    ]

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    normalized_search = search_text.strip().casefold()

    if not normalized_search:
        return []

    return [
        book_id
        for book_id, book in books.items()
        if normalized_search
        in str(book.get("title", "")).casefold()
    ]
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    normalized_borrower = borrower.strip()

    if not normalized_borrower:
        return "EMPTY_NAME"

    book = books[book_id]
    already_on_loan = any(
        str(loan.get("book_id", "")).casefold()
        == str(book_id).casefold()
        for loan in loans
    )

    if not book.get("available", False) or already_on_loan:
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": normalized_borrower
    })

    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    normalized_borrower = borrower.strip()

    if not normalized_borrower:
        return "EMPTY_NAME"

    matching_loan = None

    for loan in loans:
        same_book = (
            str(loan.get("book_id", "")).casefold()
            == str(book_id).casefold()
        )
        same_borrower = (
            str(loan.get("borrower", "")).strip().casefold()
            == normalized_borrower.casefold()
        )

        if same_book and same_borrower:
            matching_loan = loan
            break

    if matching_loan is None:
        return "NOT_ON_LOAN"

    loans.remove(matching_loan)
    books[book_id]["available"] = True

    return "OK"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    filename = Path(__file__).with_name("library.json")
    data = load_library(filename)
    books = data.get("books", {})
    loans = data.get("loans", [])

    while True:
        print("LIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            search_text = input("Enter a title or part of a title: ")
            matches = search_by_title(books, search_text)
            _display_matches(books, matches)

        elif choice == "2":
            category = input("Enter a category: ")
            matches = books_in_category(books, category)
            _display_matches(books, matches)

        elif choice == "3":
            search_text = input("Enter a book ID, title, or author: ")
            borrower = input("Enter the borrower's name: ")
            result = borrow_book(
                books,
                loans,
                search_text,
                borrower
            )
            print(result)

        elif choice == "4":
            search_text = input("Enter a book ID, title, or author: ")
            borrower = input("Enter the borrower's name: ")
            result = return_book(
                books,
                loans,
                search_text,
                borrower
            )
            print(result)

        elif choice == "5":
            save_library(data, filename)
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose an option from 1 to 5.")

        print()


def _display_matches(books, book_ids):
    if not book_ids:
        print("No matching books found.")
        return

    for book_id in book_ids:
        book = books[book_id]
        status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
        print(f"{book_id} | {book.get('title', '')} | {status}")


if __name__ == "__main__":
    main()

