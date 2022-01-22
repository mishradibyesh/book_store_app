"""
@author: Dibyesh Mishra
@date: 20-01-2022 16:51
"""
from fastapi import FastAPI, Header
import logging
from queries import Functionality
from user_model import User
from token_registeration import TokenForLogin


logging.basicConfig(filename="mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

app = FastAPI()
function = Functionality()
token_functionality = TokenForLogin()


@app.get("/users/all_users_list")
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


@app.get("/user/")
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


@app.post("/user/registration")
async def add_user(user: User):
    """
    desc: created api to add one user to the database
    param: employee class which have all the attributes related to user
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


@app.post("/user/verification/{token}")
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


@app.put("/user/update_user/")
async def update_user(user_id: int, user: User):
    """
    desc: created api to update name , email password and mobile of user to the database
    param: user id and user model
    return: updated user details in SMD format
    """
    try:
        function.show_user_data(user_id)
        result = function.update_user(user_id, user.user_name, user.user_password, user.user_email, user.mobile)
        logging.info(f"updated gender of Employee_id {user_id} ")
        return {"status": 200, "message": "Successfully updated the user Details", "data ": result}
    except Exception as error:
        logging.error(f"error caught :{error}")
        return {"status": 500, "message": f"Error : {error}"}


@app.delete("/user/delete/{user_id}")
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
