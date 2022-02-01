"""
@author: Dibyesh Mishra
@date: 01-02-2022 08:16
"""
from fastapi import APIRouter, Header
import logging
from service.queries_order import OrderFunctionality
from service.queries_cart import CartFunctionality
from schema.order_model import Order

route = APIRouter(prefix="/order", tags=["ORDER"])
funct = CartFunctionality()
obj = OrderFunctionality()


@route.post("/")
def place_order(order: Order, token: str = Header(None)):
    """
        desc: api to place an order
        :param cart: class Order object having state as address
        :param token: decoded user id after verification
        :return:result message in smd format
    """
    try:
        user_id = funct.verify_user(token)

        result = obj.place_an_order(order.address, user_id)
        logging.info("Order placed successfully")
        logging.debug(f"Order placed for User id  is : {user_id}")
        return {"status": 200, "message": f"Order placed successfully result{result}"}
    except Exception as error:
        logging.error(f"Error: {error}")
        return {"status": 404, "message": f"Error : {error}"}