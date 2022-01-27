"""
@author: Dibyesh Mishra
@date: 26-01-2022 20:53
"""
import logging
from fastapi import APIRouter, Header
from jwt_token.token_registeration import TokenForLogin
from service.queries_user import UserFunctionality
from service.queries_wishlist import WishlistFunctionality
from schema.wislist_model import Wishlist
route = APIRouter(prefix="/wishlist", tags=["WISHLIST"])
function = UserFunctionality()
token_functionality = TokenForLogin()

logging.basicConfig(filename="../mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

funct = WishlistFunctionality()


@route.get("/all/")
def get_all_wishlist(token: str = Header(None)):
    try:
        wish_list = funct.get_user_wishlist(token)
        logging.info("Successfully Get All Books From Wishlist")
        logging.debug(f"User Details are : {wish_list}")
        return {"status": 200, "message": "Successfully fetched wishlist", "data": wish_list}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
                }


@route.post("/add/")
def add_to_wishlist(wishlist: Wishlist, token: str = Header(None)):
    try:
        wish_list = funct.add_wishlist(token, wishlist.book_id)
        logging.info("Successfully added Books to Wishlist")
        logging.debug(f"User Details are : {wish_list}")
        return {"status": 200, "message": "Successfully added to  wishlist", "data": wish_list}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
        }


@route.delete("/delete/")
def delete_from_wishlist(wishlist: Wishlist, token: str = Header(None)):
    try:
        user_id = funct.delete_wishlist(token,wishlist.book_id)
        logging.info(f"Successfully deleted  Wishlist with user id{user_id}")
        return {"status": 200, "message": "Successfully deleted  wishlist", "user id": user_id}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
        }
