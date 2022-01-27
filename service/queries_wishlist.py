"""
@author: Dibyesh Mishra
@date: 26-01-2022 20:53
"""
import logging

from functools import wraps
from jwt_token.token_registeration import TokenForLogin
from fastapi import Request
from core.connection import DbConnection
from service.queries_user import UserFunctionality
from custom_exceptions.custom_exception import DataNotFound
jwt_token = TokenForLogin()
user_function = UserFunctionality()


class WishlistFunctionality:
    """
         class Functionality have methods which helping to manipulate the books table
         in database book_store_app
         """
    connection = DbConnection.establish_connection()
    my_cursor = connection.cursor(dictionary=True)

    def verify_user(self, token):
        user_id = jwt_token.decode_id(token)
        data = user_function.show_user_data(user_id)
        if data:
            return user_id
        else:
            raise DataNotFound("invalid token ")

    def get_user_wishlist(self,token):
        """
            desc: query to get all wishlist detail from database
            return: wishlist detail in dictionary format
        """
        user_id = self.verify_user(token)
        get_wishlist_query = '''select title,author,price,image from books
                                    inner join wishlist on wishlist.book_id = books.id where user_id=%d;''' % user_id
        self.my_cursor.execute(get_wishlist_query)
        wish_list = [i for i in self.my_cursor]
        if wish_list:
            return wish_list
        else:
            raise Exception("There is no result for this user_id")

    def add_wishlist(self, token, book_id):
        """
            desc: query to get all wishlist detail from database
            return: wishlist detail in dictionary format
        """
        user_id = self.verify_user(token)
        get_wishlist_query = "insert into wishlist(user_id,book_id) values(%d,%d)" % (user_id, book_id)
        self.my_cursor.execute(get_wishlist_query)
        self.connection.commit()

    def delete_wishlist(self, token, book_id):
        """
            desc: query to delete the wishlist for a user_id from database
            return: wishlist detail in dictionary format
        """
        user_id = self.verify_user(token)
        delete_wishlist_query = "delete from wishlist where user_id=%d and book_id = %d" % (user_id,book_id)
        self.my_cursor.execute(delete_wishlist_query)
        self.connection.commit()
