"""
@author: Dibyesh Mishra
@date: 20-01-2022 16:51
"""
import uvicorn
from fastapi import FastAPI, Header
import logging

from schema.book_model import Book
from service.queries import Functionality
from schema.user_model import User
from jwt_token.token_registeration import TokenForLogin


logging.basicConfig(filename="mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

app = FastAPI()
function = Functionality()
token_functionality = TokenForLogin()


@app.get("/users/all_users", tags=["USERS"])
async def get_table_data():
    """
    desc: created an api to retrieve all the data in the user table
    return: user details
    """
    try:
        result = function.show_table_data()
        logging.info("Successfully retrieved all users Details ")
        return {"status": 200, "message": "Successfully retrieved  all users Details", "data": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.get("/user/", tags=["USERS"])
async def get_user_by_id(user_id: int):
    """
    desc: created an api to retrieve all the data of a user
    param: user_id which is unique for each employee
    return: user details in SMD format
    """
    try:
        result = function.show_user_data(user_id)
        logging.info("Successfully retrieved  user Details")
        return {"status": 200, "message": "Successfully retrieved  user Details", "data": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.post("/user/registration", tags=["USERS"])
async def add_user(user: User):
    """
    desc: created api to add one user to the database
    param: User class which have all the attributes related to user
    return: user inserted details
    """
    try:
        user_id = function.add_user_db(user.user_name, user.user_password, user.user_email, user.mobile)
        logging.info("Successfully added one user Details")
        token_user = token_functionality.encode_id(user_id)
        return {"status": 200, "message": "Successfully added The user Details","token generated ": token_user,
                "data": user}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.post("/user/verification/{token}", tags=["USERS"])
async def user_verification(token: str = Header(None)):
    """
       desc: created api to verify  with token
       param: token generated at the time of adding user
       return: verification status
       """
    try:
        user_id = token_functionality.decode_id(token)
        function.verify_user(user_id)
        return {"status": 200, "message": "successfully verified"}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.put("/user/update_user/", tags=["USERS"])
async def update_user(user_id: int, user: User):
    """
    desc: created api to update name , email password and mobile of user to the database
    param: user id and user model
    return: updated user details in SMD format
    """
    try:
        function.show_user_data(user_id)
        result = function.update_user(user_id, user.user_name, user.user_password, user.user_email, user.mobile)
        logging.info(f"updated details of user_id {user_id} ")
        return {"status": 200, "message": "Successfully updated the user Details", "data ": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.delete("/user/delete/{user_id}", tags=["USERS"])
async def delete_user_by_id(user_id: int):
    """
    desc: created api to delete one user to the database
    param: user_id as path parameter
    return: deleted user details or error
    """
    try:
        function.delete_user(user_id)
        logging.info(f"deleted user by using user_id {user_id}")
        return {"status": 200, "message": "Successfully deleted one user Details",
                "data": f"deleted user id = {user_id}"}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.post("/user/login/", tags=["USERS"])
def user_login(email_id: str, password: str):
    """
    desc: created api to login into book store app
    param: user_id and user_email
    return: user details in SMD format
    """
    try:
        user_details = function.login_into_book_store(email_id, password)
        logging.info("Successfully Login into Book Store App!!")
        logging.debug(f"User Details are : {user_details}")
        user_token = token_functionality.encode_id(user_details[0]["user_id"])
        return {"status": 200, "message": "Successfully Generated the token", "token": user_token, "data": user_details}
    except Exception as e:
        logging.error(f"Error: {e}")


@app.get("/books/all_books", tags=["BOOKS"])
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


@app.get("/books/", tags=["BOOKS"])
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


@app.post("/books/add_book", tags=["BOOKS"])
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


@app.put("/book/update_book/", tags=["BOOKS"])
async def update_user(book_id: int, book: Book):
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


@app.delete("/book/delete/", tags=["BOOKS"])
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)