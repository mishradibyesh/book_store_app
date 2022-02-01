"""
@author: Dibyesh Mishra
@date: 01-02-2022 22:10
"""
import pytest
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


class TestForWishlistApi:
    """
    this class have test cases for wishlist API
    """
    def test_all_data_in_wishlist_if_retrieved(self):
        response = client.get("/wishlist/all/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully fetched wishlist"

    def test_all_data_in_wishlist_if_not_retrieved(self):
        response = client.get("/wishlist/all/", headers={
            "token": "OiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"})
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully fetched wishlist"

    @pytest.mark.parametrize('wishlist_data', [
        {"book_id": 8}])
    def test_if_book_added_to_wishlist(self, wishlist_data):
        response = client.post("/wishlist/add/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=wishlist_data)
        assert response.json()["message"] == "Successfully added to  wishlist"

    @pytest.mark.parametrize('wishlist_data', [
        {"book_id": 8}])
    def test_if_book_not_added_to_wishlist(self, wishlist_data):
        response = client.post("/wishlist/add/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=wishlist_data)
        assert response.json()["message"] != "Successfully added to  wishlist"

    @pytest.mark.parametrize('wishlist_data', [
        {"book_id": 8}])
    def test_delete_from_wishlist(self, wishlist_data):
        response = client.delete("/wishlist/delete/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=wishlist_data)
        assert response.json()["message"] == "Successfully deleted  book from cart for"

    @pytest.mark.parametrize('wishlist_data', [
        {"book_id": 9}])
    def test_if_delete_not_done_from_wishlist(self, wishlist_data):
        response = client.delete("/wishlist/delete/", headers={
            "token": "eyiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=wishlist_data)
        assert response.json()["message"] != "Successfully deleted  book from cart for"