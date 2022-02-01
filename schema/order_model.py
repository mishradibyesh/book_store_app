"""
@author: Dibyesh Mishra
@date: 01-02-2022 08:17
"""
from pydantic import BaseModel


class Order(BaseModel):
    """
    Contains address model
    """
    address: str