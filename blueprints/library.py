from app import database
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.book import Book
from models.user import User

library = Blueprint("library_blueprint", __name__, url_prefix="/library")


@library.route("/all", methods=["GET"])
@login_required
def all_books():
    """
    Query the database for all books, plus user information for users that currently have a book borrowed.
    Returns:
        (html) returns book & borrower information as HTML template.
    """
    books = database.session.query(Book, User).outerjoin(User, Book.borrower == User.email_address).all()

    if books:
        return render_template("books_and_borrower.html",
                                books=books)
    else:
        return render_template('response.html',
                               response_message="There is no books in the database.")


@library.route("/available", methods=["GET"])
@login_required
def available_books():
    """
    Query the database for all available books, by checking if the is_borrowed tag is false.
    Returns:
        (html) returns available books HTML template.
    """
    books = Book.query.filter_by(is_borrowed=False).all()

    if books:
        return render_template("books.html",
                                books=books)
    else:
        return render_template('response.html',
                               response_message="There are no books available.")


@library.route("/borrowed", methods=["GET"])
@login_required
def borrowed_books():
    """
    Query all borrowed books, plus user information for users that have a book borrowed.
    Returns:
        (html) returns borrowed books HTML template.
    """
    books = (database.session.query(Book, User)
             .join(User, Book.borrower == User.email_address)
             .filter(Book.is_borrowed == True)
             .all())
    if books:
        return render_template("books_and_borrower.html",
                               books=books)
    else:
        return render_template('response.html',
                        response_message="There are no borrowed books.")


@library.route("/due", methods=["GET"])
@login_required
def due_today():
    """
    Check for overdue books that match today's date, or a date in the past
    and compare that to the current logged-in user's borrowed books.
    Returns:
        (html) returns due/overdue books HTML template.
        (str) messaging saying that no books are due to be returned.
    """
    current_date = datetime.now().date()

    books = (Book.query.filter_by(
        is_borrowed=True,
        borrower=current_user.email_address)
             .filter(Book.return_date <= current_date)
             .all())

    if books:
        return render_template("books_due.html",
                               books=books)
    else:
        return render_template('response.html',
                               response_message="No books are due to be returned today.")


@library.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow_book():
    """
    Allow the user to search for a book within the database, then select a book from the returned list of books
    to borrow it, setting the return date for 7 days in the future.
    Returns:
        (html) returns HTML template for borrowing books.
        (str) error message indicating that the book could not be found.
    """
    matching_books = []

    if request.method == "POST" and "selected_book" in request.form:
        selected_book_title = request.form["selected_book"]
        selected_book = Book.query.filter_by(title=selected_book_title).first()

        if selected_book:
            selected_book.is_borrowed = True
            selected_book.borrower = current_user.email_address
            selected_book.return_date = datetime.now().date() + timedelta(days=7)

            database.session.commit()

            return render_template('response.html',
                                   response_message=f"You ({selected_book.borrower}) have "
                                                    f"borrowed '{selected_book.title}'"
                                                    f"please return by {selected_book.return_date}.")

    if request.method == "GET":
        matching_books = Book.query.filter_by(is_borrowed=False).all()

        # if there are no available books return an error message.
        if matching_books is None:
            return render_template('response.html',
                                   response_message="Sorry! There are no available books at the moment.")

    return render_template("borrow.html",
                           books=matching_books)
