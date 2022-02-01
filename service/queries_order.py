"""
@author: Dibyesh Mishra
@date: 01-02-2022 08:18
"""
from core.connection import DbConnection


class OrderFunctionality:
    """
         class Functionality have methods which helping to manipulate the order table
         in database book_store_app
         """
    connection = DbConnection.establish_connection()
    my_cursor = connection.cursor(dictionary=True)

    def place_an_order(self, address, user_id):
        """
            desc: place order
            param:  address, book_id
            :return: order_id
        """
        # query = f"CALL sp_order(%d,'%s')" % (user_id, address)
        args = [user_id, f'{address}']
        result_args = self.my_cursor.callproc('sp_order', args)
        self.connection.commit()
        return result_args
