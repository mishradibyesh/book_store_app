"""
@author: Dibyesh Mishra
@date: 26-01-2022 14:36
"""
import logging
from fastapi import APIRouter, Header
from jwt_token.token_registeration import TokenForLogin
from schema.user_model import User
from send_email import send_email_async
from service.queries_user import UserFunctionality

route = APIRouter(prefix="/users", tags=["USERS"])
function = UserFunctionality()
token_functionality = TokenForLogin()

logging.basicConfig(filename="../mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')


@route.get("/all/")
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


@route.get("/")
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


@route.post("/registration")
async def add_user(user: User):
    """
    desc: created api to add one user to the database
    param: User class which have all the attributes related to user
    return: user inserted details
    """
    try:
        user_id = function.add_user_db(user.user_name, user.user_password, user.user_email, user.mobile)
        logging.info("Successfully added one user Details")
        token_user = token_functionality.encode_id_without_expire_time(user_id)
        await send_email_async("user_verification", user.user_email, token_user)
        return {"status": 200, "message": "Successfully added The user Details and sent the mail","token generated ": token_user,
                "data": user}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@route.get("/verification/{token}")
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


@route.put("/")
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


@route.delete("/delete/{user_id}")
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


@route.post("/login/")
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
        user_token = token_functionality.encode_id_with_expiry(user_details[0]["user_id"])
        return {"status": 200, "message": "Successfully Generated the token", "token": user_token, "data": user_details}
    except Exception as e:
        logging.error(f"Error: {e}")

