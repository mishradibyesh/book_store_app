"""
@author: Dibyesh Mishra
@date: 20-01-2022 15:46
"""
import logging
import os

from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()
logging.basicConfig(filename="mylog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')


class DbConnection:
    """
    this class contains a method which is establishing a
    connection with database online_book_store
    """

    @staticmethod
    def establish_connection():
        """
        desc: Establish connection with database
        return: connection
        """
        try:
            mydb = connect(
                host="localhost",
                user=os.getenv('user1'),
                passwd=os.getenv('passwrd'),
                database=os.getenv('database_name')
            )
            logging.info("Connection to database has been established successfully")
            return mydb
        except Error as e:
            logging.error("Connection is somehow not established")
            print(e)

