"""
@author: Dibyesh Mishra
@date: 27-01-2022 22:14
"""
import logging
from fastapi import APIRouter, Header
from jwt_token.token_registeration import TokenForLogin
from schema.cart_model import Cart
from service.queries_user import UserFunctionality
from service.queries_cart import CartFunctionality
from schema.wislist_model import Wishlist
route = APIRouter(prefix="/cart", tags=["CART"])
function = UserFunctionality()
token_functionality = TokenForLogin()

logging.basicConfig(filename="../mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

funct = CartFunctionality()


@route.get("/all/")
def get_cart_items(token: str = Header(None)):
    try:
        cart = funct.get_user_cart(token)
        logging.info("Successfully Get All Books details in cart")
        return {"status": 200, "message": "Successfully fetched wishlist", "data": cart}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
                }


@route.post("/add/")
def add_to_cart(cart: Cart, token: str = Header(None)):
    try:
        cart = funct.add_to_cart(token, cart.book_id, cart.quantity)
        logging.info("Successfully added  to cart")
        return {"status": 200, "message": "Successfully added to  cart", "data": cart}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
        }

@route.put("/")
def update_quantity(cart: Cart, token: str = Header(None)):
    """
    desc: api to update book quantity in cart
    :param cart: class Cart object having states book_id and quantity
    :param token: decoded user id after verification
    :return: book id with updated quantity of books in SMD format
    """
    try:
        updated_quantity = funct.update_quantity_of_book_in_cart(token, cart.book_id, cart.quantity)
        logging.info("Successfully Updated Book Quantity In Cart")
        logging.debug(f"Updated book quantity ")
        return {"status": 200, "message": "Successfully Updated Book Quantity In Cart",
                "updated quantity": updated_quantity}
    except Exception as error:
        logging.error(f"Error: {error}")
        return {"status": 404, "message": f"Error : {error}"}


@route.delete("/delete/")
def delete_from_wishlist(book_id: int, token: str = Header(None)):
    try:
        funct.delete_wishlist(token,book_id)
        logging.info("Successfully deleted  book from cart")
        return {"status": 200, "message": "Successfully deleted  book from cart", "book id": book_id}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": 404, "message": f"Error : {e}"
        }
