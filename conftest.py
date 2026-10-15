import random

import pytest
import requests

from config import *
from faker import Faker
from models.user_dto import UserDTO

fake = Faker()

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL + API_VERSION


@pytest.fixture(scope="session")
def registration_url():
    return BASE_URL + API_VERSION + REGISTRATION_URL

@pytest.fixture(scope="session")
def login_url():
    return BASE_URL + API_VERSION + LOGIN_URL

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s
    s.close()

@pytest.fixture(scope="function")
def random_user():
    username = f"qa_{fake.email()}"
    password = fake.password(
        length=random.randint(8, 20),
        digits=True,
        upper_case=True,
        lower_case=True,
        special_chars=False,
    )+"$"
    return UserDTO(
        username=username,
        password=password,
        firstName=fake.first_name(),
        lastName=fake.last_name(),
    )




