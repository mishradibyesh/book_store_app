"""
@author: Dibyesh Mishra
@date: 20-01-2022 20:12
"""
import time

import jwt


class TokenForLogin:
    """
    this class has methods which have functionalities like encode and decode
    """
    def encode_id_with_expiry(self, user_id):
        """
        desc: encoding the employee_id with expire time
        param: employee_id:
        return: generated_token
        """
        payload = {"id": user_id, "expires": time.time()+60}
        token_generated = jwt.encode(payload, "secret_code")
        return token_generated

    def encode_id_without_expire_time(self, user_id):
        """
        desc: encoding the employee_id
        param: employee_id:
        return: generated_token
        """
        payload = {"id": user_id}
        token_generated = jwt.encode(payload, "secret_code")
        return token_generated

    def decode_id(self, token):
        """
        desc: decoding the user_id
        param: user_id:
        return: decoded user id
        """
        payload = jwt.decode(token, "secret_code", algorithms=["HS256"])
        return payload.get('id')