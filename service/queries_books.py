"""
@author: Dibyesh Mishra
@date: 26-01-2022 14:49
"""
import logging
from io import StringIO

from core.connection import DbConnection
from custom_exceptions.custom_exception import DataNotFound
import pandas as pd


class BooksFunctionality:
    """
      class BooksFunctionality have methods which helping to manipulate the books table
      in database book_store_app
      """
    connection = DbConnection.establish_connection()
    my_cursor = connection.cursor(dictionary=True)

    def show_all_books(self):
        """
        desc: displaying the book details
        return: data_list containing all books details
        """

        query = "select * from books "
        self.my_cursor.execute(query)
        data_list = [i for i in self.my_cursor]
        print(data_list)
        if data_list:
            return data_list
        else:
            raise DataNotFound("table is not present in the database")

    def show_book_data(self, book_id):
        """
        desc: displaying the book_detail
        param: book_id
        return: data_list or error
        """
        query = "select * from books where id = %d" % book_id
        self.my_cursor.execute(query)
        data_list = [i for i in self.my_cursor]
        if data_list:
            return data_list
        else:
            raise DataNotFound("this book id is not present in the database")

    def add_book_to_db(self, id, author, title, image, quantity, price, description):
        """
        desc: adding book details in  the user table
        param : id, author, title, image, quantity, price, description
        return: result
        """
        query = "insert into books (id, author, title, image, quantity, price, description) values" \
                " (%d, '%s', '%s', '%s', %d ,%f,'%s')" % (id, author, title, image, quantity, price, description)
        self.my_cursor.execute(query)
        self.connection.commit()
        result = self.show_book_data(id)
        return result

    def update_book(self, book_id, id, author, title, image, quantity, price, description):
        """
        desc: updating  id, author, title, image, quantity, price, description in  the books table
        param:  id, author, title, image, quantity, price, description
        return: updated data or error
        """
        query = "update books set id = %d, author = '%s', title='%s', image='%s',quantity=%d, price = %f, " \
                "description = '%s' where id = %d" \
                % (id, author, title, image, quantity, price, description, book_id)
        self.my_cursor.execute(query)
        self.connection.commit()
        updated_data = self.show_book_data(id)
        return updated_data

    def delete_book(self, book_id):
        """
        desc: deleting book details from the database
        param: book_id
        """
        self.show_book_data(book_id)
        query = "delete from books where id = %d" % book_id
        self.my_cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query, values=None):
        """
            to take sql query and execute it
            :param query: query to be executed
            :return: None
         """
        try:
            if not values:
                self.my_cursor.execute(query)
            else:
                self.my_cursor(query, values)
            self.connection.commit()
        except Exception as e:
            logging.error(str(e))
            self.connection.rollback()

    def insert_to_db(self, csv_file):
        """
        desc: to read csv and push it to database
        param: csvfile: path of csv file
        return: message
        """
        books_dataframe = pd.read_csv(StringIO(str(csv_file.file.read(), 'utf-8')), encoding='utf-8')
        cols = ", ".join([str(i) for i in books_dataframe.columns.tolist()])
        for i, row in books_dataframe.iterrows():
            sql = "INSERT INTO books (" + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)"
            self.my_cursor.execute(sql, tuple(row))
            self.connection.commit()
        return "Books are Added Successfully!!"