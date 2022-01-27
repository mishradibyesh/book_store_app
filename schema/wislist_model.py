"""
@author: Dibyesh Mishra
@date: 27-01-2022 13:08
"""
from pydantic import BaseModel


class Wishlist(BaseModel):
    """
    this class contains attributes related to employee details
    """
    book_id: int