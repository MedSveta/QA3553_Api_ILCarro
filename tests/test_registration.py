from dataclasses import asdict
import pytest

from models.user_dto import UserDTO


class TestRegistration:
    def test_registration_positive(self, session, registration_url, random_user):
        body = asdict(random_user)

        response = session.post(registration_url, json=body)
        assert response.status_code == 200, "fail"
        assert "accessToken" in response.json()

    def test_registration_negative_duplicate_user(self, session, registration_url, random_user):
        body = asdict(random_user)

        first = session.post(registration_url, json=body)
        assert first.status_code == 200, "fail"

        response = session.post(registration_url, json=body)
        print(response.status_code)
        assert response.status_code in [400, 409], "fail"


    @pytest.mark.parametrize("invalid_email", [
        "wrong123test.gmail.com",
        "cvdfrt456@vbghycom",
        "йцукены3456@gmail.com",
        "",
        "rtfygh567@@bnhj.com",
        "cvfgrty?jki45@bnhm.com",
        "ghyujbt56@fgrt..com",
        "cvfbgytu45 2vbh@vbg.com",
        "@vbg.com",
        "vbgnhjuk6785@",
        "34@456.67",
    ])
    def test_registration_negative_invalid_email(self, session, registration_url, invalid_email):
        user = UserDTO(invalid_email, "Qwerty123$", "Sveta", "QA")
        body = asdict(user)
        response = session.post(registration_url, json=body)
        assert response.status_code == 400, "fail"


