"""
@author: Dibyesh Mishra
@date: 27-01-2022 22:13
"""
from jwt_token.token_registeration import TokenForLogin
from core.connection import DbConnection
from service.queries_user import UserFunctionality
from custom_exceptions.custom_exception import DataNotFound
jwt_token = TokenForLogin()
user_function = UserFunctionality()


class CartFunctionality:
    """
         class Functionality have methods which helping to manipulate the wishlist table
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

    def get_user_cart(self,token):
        """
            desc: query to get cart detail from database
            return: cart detail in dictionary format
        """
        user_id = self.verify_user(token)
        get_cart_query = '''select books.id,title,author,price,image,cart.user_id,cart.quantity from books
                                    inner join cart on cart.book_id = books.id where user_id=%d;''' % user_id
        self.my_cursor.execute(get_cart_query)
        wish_list = [i for i in self.my_cursor]
        if wish_list:
            return wish_list
        else:
            raise Exception("There is no result for this user_id")

    def add_to_cart(self, token, book_id, quantity):
        """
            desc: query to get all wishlist detail from database
            return: wishlist detail in dictionary format
        """
        user_id = self.verify_user(token)
        get_wishlist_query = "insert into cart(book_id,user_id,quantity) values(%d,%d,%d)" % (book_id, user_id,quantity)
        self.my_cursor.execute(get_wishlist_query)
        self.connection.commit()

    def update_quantity_of_book_in_cart(self,token, book_id, quantity):
        """
            desc: deleting book from cart
            param:  user_id, book_id
            :return: quantity
        """
        user_id = self.verify_user(token)
        query = "UPDATE cart SET quantity = %d WHERE book_id = %d AND user_id = %d" % (quantity, book_id, user_id)
        self.my_cursor.execute(query)
        self.connection.commit()
        return quantity

    def delete_cart(self, token, book_id):
        """
            desc: query to delete the book for a user_id from cart
            param: token , book_id
        """
        user_id = self.verify_user(token)
        delete_wishlist_query = "delete from cart where user_id=%d and book_id = %d" % (user_id,book_id)
        self.my_cursor.execute(delete_wishlist_query)
        self.connection.commit()
