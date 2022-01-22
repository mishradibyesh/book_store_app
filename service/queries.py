"""
@author: Dibyesh Mishra
@date: 20-01-2022 16:57
"""
from connection import DbConnection
from custom_exception import DataNotFound


class Functionality:
    """
    class Functionality have methods which helping to manipulate the database table employee_details
    in database employee_payroll
    """
    connection = DbConnection.establish_connection()
    my_cursor = connection.cursor(dictionary=True)

    def show_table_data(self):
        """
        desc: displaying the employee_details table
        return: data_list
        """

        query = "select * from user "
        self.my_cursor.execute(query)
        data_list = [i for i in self.my_cursor]
        if data_list:
            return data_list
        else:
            raise DataNotFound("table  is not present in the database")

    def show_user_data(self, user_id):
        """
        desc: displaying the employee_detail
        param: employee_id
        return: data_list or error
        """
        query = "select * from user where user_id = %d" % user_id
        self.my_cursor.execute(query)
        data_list = [i for i in self.my_cursor]
        if data_list:
            return data_list
        else:
            raise DataNotFound("this id is not present in the database")

    def get_user_id(self, user_email):
        """
        desc: displaying the employee_detail
        param: employee_id
        return: data_list or error
        """
        query = "select user_id from user where user_email = '%s'" % user_email
        self.my_cursor.execute(query)
        user_id = [i for i in self.my_cursor]
        if user_id:
            return user_id[0]["user_id"]
        else:
            raise DataNotFound("this email id  is not present in the database")

    def add_user_db(self, user_name, user_password, user_email, mobile):
        """
        desc: adding user details in  the user table
        param : user_id, user_name, user_password, user_email, mobile, is_verified
        return: message string
        """
        query = "insert into user (user_name, user_password, user_email, mobile) values" \
                " ('%s', '%s', '%s', %d)" % (
                     user_name, user_password, user_email, mobile )
        self.my_cursor.execute(query)
        self.connection.commit()
        user_id = self.get_user_id(user_email)
        return user_id

    def verify_user(self, user_id):
        """
        desc: verify user details from the database
        param: user_id
        """
        query = "update user set is_verified = true where user_id = %d" % user_id
        self.my_cursor.execute(query)
        self.connection.commit()

    def update_user(self, user_id, user_name, user_password, user_email, mobile):
        """
        desc: updating user name , password , email and mobile in  the employee_details table
        param: salary, employee_name
        return: updated data or error
        """
        query = "update user set user_name = '%s', user_password='%s', user_email='%s', mobile = %d where user_id = %d"\
                % (user_name, user_password, user_email, mobile,user_id)
        self.my_cursor.execute(query)
        self.connection.commit()
        updated_data = self.show_user_data(user_id)
        return updated_data

    def delete_user(self, user_id):
        """
        desc: deleting user details from the database
        param: user_id
        """
        self.show_user_data(user_id)
        query = "delete from user where user_id = %d" % user_id
        self.my_cursor.execute(query)
        self.connection.commit()
