"""
@author: Dibyesh Mishra
@date: 01-02-2022 23:24
"""
import pytest
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


class TestForCartApi:
    """
    this class have test cases for cart API
    """
    def test_all_data_in_cart_if_retrieved(self):
        response = client.get("/cart/all/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully fetched cart"

    def test_if_token_is_not_valid(self):
        response = client.get("/cart/all/", headers={
            "token": "V1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully fetched cart"

    @pytest.mark.parametrize('cart_data', [
        {"book_id": 8, "quantity":1}])
    def test_if_book_added_to_cart(self, cart_data):
        response = client.post("/cart/add/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=cart_data)
        assert response.json()["message"] == "Successfully added to  cart"

    @pytest.mark.parametrize('cart_data', [
        {"book_id": 65, "quantity": 1}])
    def test_if_book_not_added_to_cart(self, cart_data):
        response = client.post("/cart/add/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=cart_data)
        assert response.json()["message"] != "Successfully added to  cart"

    @pytest.mark.parametrize('cart_data', [
        {"book_id": 8, "quantity": 2}])
    def test_if_book_details_are_updated_to_cart(self, cart_data):
        response = client.put("/cart/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=cart_data)
        assert response.json()["message"] == "Successfully Updated Book Quantity In Cart"

    @pytest.mark.parametrize('cart_data', [
        {"book_id": 2, "quantity": 2}])
    def test_if_book_details_are_not_updated_to_cart(self, cart_data):
        response = client.put("/cart/", headers={
            "token": "eyJ0iJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=cart_data)
        assert response.json()["message"] != "Successfully Updated Book Quantity In Cart"

    @pytest.mark.parametrize('book_id', [8])
    def test_delete_from_cart(self, book_id):
        response = client.delete(f"/cart/delete/?book_id={book_id}", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.json()["message"] == "Successfully deleted  book from cart"

    @pytest.mark.parametrize('book_id', [9])
    def test_if_delete_not_done_from_cart(self, book_id):
        response = client.delete(f"/cart/delete/?book_id={book_id}", headers={
            "token": "eyiOiJKV1QiLCJhbGciOiJIUI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.json()["message"] != "Successfully deleted  book from cart"