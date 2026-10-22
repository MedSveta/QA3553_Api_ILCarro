from dataclasses import asdict

from requests import session

from conftest import add_new_car_url


class TestCars:
    def test_add_new_car_positive(self, session, add_new_car_url, random_car, auth_header):
        response = session.post(add_new_car_url, headers=auth_header, json=asdict(random_car))
        assert response.status_code == 200

    def test_add_new_car_wo__header_auth_negative(self, session, add_new_car_url, random_car):
        response = session.post(add_new_car_url, json=asdict(random_car))
        assert response.status_code == 403

    def test_get_all_user_cars_positive(self, session, get_all_user_cars_url, auth_header):
        response = session.get(get_all_user_cars_url, headers=auth_header)
        assert response.status_code == 200

    def test_get_all_user_cars_wrong_token_negative(self, session, get_all_user_cars_url, auth_header):
        headers = {"Authorization": "Bearer drftrygy"}
        response = session.get(get_all_user_cars_url, headers=headers)
        print(response.json())
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"
        assert "strings must contain exactly 2 period characters" in response.json()["message"]

    def test_delete_user_car_positive(self, session, delete_car_url, add_new_car_url, auth_header, random_car):
        session.post(add_new_car_url(), json=asdict(random_car), headers=auth_header)
        serial_number = random_car["serialNumber"]
        response = session.delete(delete_car_url + serial_number, headers=auth_header)
        assert response.status_code == 200
