from dataclasses import asdict

class TestRegistration:
    def test_registration_positive(self, session, registration_url, random_user):
        body = asdict(random_user)

        response = session.post(registration_url, json=body)
        assert response.status_code == 200
        assert "accessToken" in response.json()



