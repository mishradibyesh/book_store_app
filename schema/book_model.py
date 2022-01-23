"""
@author: Dibyesh Mishra
@date: 23-01-2022 17:31
"""
from pydantic import BaseModel


class Book(BaseModel):
    """
    this class contains attributes related to book details
    """
    id: int
    author: str
    title: str
    image: str
    quantity: int
    price: float
    description: str
