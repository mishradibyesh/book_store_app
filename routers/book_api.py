"""
@author: Dibyesh Mishra
@date: 26-01-2022 14:36
"""
import logging
from fastapi import APIRouter, UploadFile, File
from jwt_token.token_registeration import TokenForLogin
from schema.book_model import Book
from service.queries_books import BooksFunctionality

route = APIRouter(prefix="/users", tags=["BOOKS"])
function = BooksFunctionality()
token_functionality = TokenForLogin()

logging.basicConfig(filename="../mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')


@route.get("/books/all_books")
async def get_table_data():
    """
    desc: created an api to retrieve all the data in the book table
    return: book details
    """
    try:
        result = function.show_all_books()
        logging.info("Successfully retrieved all books Details ")
        return {"status": 200, "message": "Successfully retrieved  all books Details", "data": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.get("/books/")
async def get_book_by_id(book_id: int):
    """
    desc: created an api to retrieve all the data of about a book
    param: book_id which is unique for each book
    return: book details in SMD format
    """
    try:
        result = function.show_book_data(book_id)
        logging.info("Successfully retrieved  book Details")
        return {"status": 200, "message": "Successfully retrieved  book Details", "data": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.post("/books/")
async def add_book(book: Book):
    """
    desc: created api to add one book to the database
    param: Book class which have all the attributes related to book
    return: book inserted details
    """
    try:
        result = function.add_book_to_db(book.id, book.author, book.title, book.image, book.quantity, book.price,book.description)
        logging.info("Successfully added one book Details")
        return {"status": 200, "message": "Successfully added The book Details","data": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.put("/book/")
async def update_book(book_id: int, book: Book):
    """
    desc: created api to update id, author, title, image, quantity, price, description of book to the database
    param: book id and book model
    return: updated book details in SMD format
    """
    try:
        result = function.update_book(book_id, book.id, book.author, book.title, book.image, book.quantity, book.price,
                                      book.description)
        logging.info(f"updated the details with book id {book_id} ")
        return {"status": 200, "message": "Successfully updated the book Details", "data ": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.delete("/book/")
async def delete_book_by_id(book_id: int):
    """
    desc: created api to delete one book from the database
    param: book_id as path parameter
    return: deleted book details or error
    """
    try:
        function.delete_book(book_id)
        logging.info(f"deleted book by using book_id {book_id}")
        return {"status": 200, "message": "Successfully deleted one book Details",
                "data": f"deleted book id = {book_id}"}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.post("/book/upload_file")
async def upload_csv_file(csv_file: UploadFile = File(...)):
    try:
        result = function.insert_to_db(csv_file)
        logging.info("successfully uploaded the file and inserted into database")
        return {"Status": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}