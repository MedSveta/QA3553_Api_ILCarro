import pytest
from config import *

class TestLogin:
    def test_login_positive(self, session,login_url, registered_user):
        body = {
            "username": registered_user.username,
            "password": registered_user.password,
        }
        response = session.post(login_url, json=body)
        assert response.status_code == 200

    @pytest.mark.parametrize("invalid_email", [
        "",
        "ghtyuui789@ghy.nju"
    ])
    def test_login_negative_wrong_email(self, session,login_url, invalid_email):
        body = {
            "username": invalid_email,
            "password": TEST_PASSWORD,
        }
        response = session.post(login_url, json=body)
        print(response.json())
        assert response.status_code in [401, 400]
        assert "Login or Password incorrect" in response.json().values()