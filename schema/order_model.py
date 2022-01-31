"""
@author: Dibyesh Mishra
@date: 30-01-2022 22:46
"""
from pydantic import BaseModel


class Order(BaseModel):
    """
    Contains address
    """
    address: str