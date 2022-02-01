"""
@author: Dibyesh Mishra
@date: 01-02-2022 04:09
"""
import pytest
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


class TestForUserApi:
    """
    this class have test cases for user API
    """
    def test_all_data_in_user_table_if_retrieved(self):
        response = client.get("/users/all/")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully retrieved  all users Details"

    def test_all_data_in_user_table_if_not_retrieved(self):
        response = client.get("/users/all/")
        assert response.status_code == 200
        assert response.json()["message"] != "data not found"

    @pytest.mark.parametrize('user_id', [2])
    def test_one_user_data(self, user_id):
        response = client.get(f"/users/?user_id={user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully retrieved  user Details"

    @pytest.mark.parametrize('user_id', [98])
    def test_one_user_data_if_not_present(self, user_id):
        response = client.get(f"/users/?user_id={user_id}")
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully retrieved  user Details"

    @pytest.mark.parametrize('user_data', [
        {"user_name": "ramuesh", "user_password": "1k23", "user_email": "abc2d@gmail.com", "mobile": 79357393}])
    def test_if_user_added_to_db(self, user_data):
        response = client.post("/users/registration/", json=user_data)
        assert response.json()["message"] == "Successfully added The user Details and sent the mail"

    @pytest.mark.parametrize('user_data', [
        {"user_name": "ramesh", "user_password": "123", "user_email": "abcd@gmail.com", "mobile": 78357393}])
    def test_if_user_is_not_added_to_db(self, user_data):
        response = client.post("/users/registration/", json=user_data)
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully added The user Details and sent the mail"

    def test_if_verification_is_successful(self):
        response = client.get(f"/users/verification/", headers={
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwaXJlcyI6MTY0MzY1NTg0Ni44OTM5MTE0fQ.kT1__XdTU_tHZmD8zCZRVWbS5Ir57ITBCPhZSskdSsg"})
        assert response.json()['message'] == "successfully verified"

    def test_if_verification_is_not_successful(self):
        response = client.get(f"/users/verification/", headers={
            "token": ".kT1__XdTU_tHZmD8zCZRVWbS5Ir57ITBCPhZSskdSsg"})
        assert response.json()['message'] != "successfully verified"

    @pytest.mark.parametrize('user_id,user_data', [
        (3,{"user_name": "shivam", "user_password": "123", "user_email": "shivammishra@gmail.com", "mobile": 78357393})])
    def test_if_user_updated_to_db(self,user_id, user_data):
        response = client.put(f"/users/?user_id={user_id}", json=user_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully updated the user Details"

    @pytest.mark.parametrize('user_id,user_data', [
        (5,{"user_name": "shivam", "user_password": "123", "user_email": "shivammishra@gmail.com", "mobile": 78357393})])
    def test_if_user_details_not_updated_to_db(self, user_id, user_data):
        response = client.put(f"/users/?user_id={user_id}", json=user_data)
        # assert response.status_code == 200
        assert response.json()["message"] != "Successfully updated the user Details"

    @pytest.mark.parametrize('user_id', [(4)])
    def test_if_employee_id_is_deleted_from_database(self, user_id):
        response = client.delete(f"/users/delete/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully deleted one user Details"

    @pytest.mark.parametrize('user_id', [(4)])
    def test_if_employee_id_is_not_deleted_from_database(self, user_id):
        response = client.delete(f"/users/delete/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] != "Successfully deleted one user Details"

    @pytest.mark.parametrize('email_id , password', [('dibyesh@gmail.com', 'Dibyesh@3')])
    def test_if_login_is_successful(self, email_id, password):
        response = client.post(f"/users/login/?email_id={email_id}&password={password}")
        assert response.json()['message'] == "Successfully logged in and  Generated the token"

    @pytest.mark.parametrize('email_id , password', [('dibyesh@gmail.com', 'dibyesh@3')])
    def test_if_login_is_not_successful(self, email_id, password):
        response = client.post(f"/users/login/?email_id={email_id}&password={password}")
        assert response.json()['message'] != "Successfully logged in and  generated the token"
