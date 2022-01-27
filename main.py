"""
@author: Dibyesh Mishra
@date: 20-01-2022 16:51
"""
import uvicorn

from routers import user_api, wishlist_api, book_api
from fastapi import FastAPI


app = FastAPI(title="Book Store App")

app.include_router(user_api.route)
app.include_router(book_api.route)
app.include_router(wishlist_api.route)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)