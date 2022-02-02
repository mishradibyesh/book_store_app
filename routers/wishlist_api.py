"""
@author: Dibyesh Mishra
@date: 26-01-2022 20:53
"""
import logging
from fastapi import APIRouter, Header
from jwt_token.token_registeration import TokenForLogin
from service.queries_wishlist import WishlistFunctionality
from schema.wislist_model import Wishlist
route = APIRouter(prefix="/wishlist", tags=["WISHLIST"])
token_functionality = TokenForLogin()

logging.basicConfig(filename="../mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

funct = WishlistFunctionality()


@route.get("/all/")
def get_all_wishlist(token: str = Header(None)):
    """
    desc: api to get all the books in the wishlist
    param: token to varify user and to get user id
    return: wishlist data
    """
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
    """
       desc: api to add the books in the wishlist
       param: token to varify user and to get user id and wishlist object
       return: wishlist data
    """
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
    """
       desc: api to delete books from the wishlist
       param: token to varify user and to get user id and wishlist
       return: deleted
    """
    try:
        book_id = funct.delete_wishlist(token,wishlist.book_id)
        logging.info(f"Successfully deleted  Wishlist with book id{book_id}")
        return {"status": 200, "message": "Successfully deleted  book from wishlist for", "book id": book_id}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
        }
