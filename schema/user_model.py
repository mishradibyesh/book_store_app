"""
@author: Dibyesh Mishra
@date: 20-01-2022 17:24
"""
from pydantic import BaseModel


class User(BaseModel):
    """
    this class contains attributes related to employee details
    """
    user_name: str
    user_password: str
    user_email: str
    mobile: int

