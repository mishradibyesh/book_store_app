"""
@author: Dibyesh Mishra
@date: 02-02-2022 22:07
"""
import pytest
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


class TestOrderApi:
    """
    this class have test cases for cart API
    """

    @pytest.mark.parametrize('order_data', [
        {"address": 'Ballia'}])
    def test_if_order_is_placed(self, order_data):
        response = client.post("/order/", headers={
            "token":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=order_data)
        assert response.json()["message"] == "Order placed successfully result{'sp_order_arg1': 1, " \
                                             "'sp_order_arg2': 'Ballia'}"

    @pytest.mark.parametrize('order_data', [
        {"address": 'Ballia'}])
    def test_if_order_is_not_placed(self, order_data):
        response = client.post("/order/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzIJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzcwMjg0OC4wOTM3Njg2fQ."
                     "P9NgeHvY06iM9Wo4TblBhkbBcMY5IWRSJr9eCwgALMk"}, json=order_data)
        assert response.json()["message"] != "Order placed successfully result{'sp_order_arg1': 1, " \
                                             "'sp_order_arg2': 'Ballia'}"
