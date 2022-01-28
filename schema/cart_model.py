"""
@author: Dibyesh Mishra
@date: 27-01-2022 22:08
"""
from pydantic import BaseModel


class Cart(BaseModel):
    """
    this class contains attributes related to cart details
    """
    book_id: int
    quantity: int

