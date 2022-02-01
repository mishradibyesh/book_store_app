"""
@author: Dibyesh Mishra
@date: 01-02-2022 16:03
"""
import pytest
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


class TestForBookApi:
    """
    this class have test cases for books API
    """
    def test_all_data_in_books_table_if_retrieved(self):
        response = client.get("/books/all_books/")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully retrieved  all books Details"

    @pytest.mark.parametrize('book_id', [2])
    def test_one_book_data_if_retrieved(self, book_id):
        response = client.get(f"/books/?book_id={book_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully retrieved  book Details"

    @pytest.mark.parametrize('book_id', [56])
    def test_one_book_data_if_not_retrieved(self, book_id):
        response = client.get(f"/books/?book_id={book_id}")
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully retrieved  book Details"

    @pytest.mark.parametrize('book_data', [
        {"id": 56, "author": "dibyesh", "title": "the village", "image": "abc.jpg",
         "quantity": 12,"price":230 , "description": "good book about village life"}])
    def test_if_book_added_to_db(self, book_data):
        response = client.post("/books/", json=book_data)
        assert response.json()["message"] == "Successfully added The book Details"

    @pytest.mark.parametrize('book_data', [
        {"id": 56, "author": "dibyesh", "title": "the village", "image": "abc.jpg",
         "quantity": 12, "price": 230, "description": "good book about village life"}])
    def test_if_book_added_to_db(self, book_data):
        response = client.post("/books/", json=book_data)
        assert response.json()["message"] != "Successfully added The book Details"

    @pytest.mark.parametrize('book_id,book_data', [
        (56,
         {"id": 56, "author": "dibyesh", "title": "the village", "image": "abc.jpg",
             "quantity": 12, "price": 230, "description": "good book about village life"})])
    def test_if_book_updated_to_db(self, book_id, book_data):
        response = client.put(f"/books/?book_id={book_id}", json=book_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully updated the book Details"

    @pytest.mark.parametrize('book_id,book_data', [
        (54,
         {"id": 54, "author": "dibyesh", "title": "the village", "image": "abc.jpg",
          "quantity": 12, "price": 230, "description": "good book about village life"})])
    def test_if_book_is_not_updated_to_db(self, book_id, book_data):
        response = client.put(f"/books/?book_id={book_id}", json=book_data)
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully updated the book Details"

    @pytest.mark.parametrize('book_id', [(56)])
    def test_if_book_id_is_not_deleted_from_database(self, book_id):
        response = client.delete(f"/books/?book_id={book_id}")
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully deleted one book Details"