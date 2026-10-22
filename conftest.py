import random
from dataclasses import asdict

import pytest
import requests

from config import *
from faker import Faker
from models.user_dto import UserDTO
from models.car_dto import CarDTO

fake = Faker()
fake_ru = Faker("ru_RU")
fake_en = Faker("en_US")


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
def add_new_car_url():
    return BASE_URL + API_VERSION + ADD_NEW_CAR_URL

@pytest.fixture(scope="session")
def delete_car_url():
    return BASE_URL + API_VERSION + DELETE_CAR_BY_SERIAL_NUMBER_URL

@pytest.fixture(scope="session")
def get_all_user_cars_url():
    return BASE_URL + API_VERSION + GET_ALL_USER_CARS_URL

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

@pytest.fixture(scope="function")
def random_user_ru():
    name_ru = fake_ru.first_name()
    username = f"qa_{name_ru}_{fake.email()}"
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

@pytest.fixture(scope="function")
def registered_user(session, registration_url, random_user):
    user_data = {
        "username": random_user.username,
        "password": random_user.password,
    }
    response_reg = session.post(registration_url, json=user_data)
    if response_reg.status_code == 200:
        return random_user
    return  UserDTO(TEST_EMAIL, TEST_PASSWORD)

@pytest.fixture(scope="function")
def auth_token(registered_user, session, login_url):
    body = asdict(registered_user)
    response = session.post(login_url, json=body)
    return response.json()["accessToken"]

@pytest.fixture(scope="function")
def random_car():
    return CarDTO(
        serialNumber=f"{str(random.randint(1, 1000))}-MSD",
        manufacture=fake.company(),
        model=fake.word().capitalize(),
        year=str(random.randint(0, 2026)),
        fuel=random.choice(["Petrol", "Diesel", "Hybrid", "Electric"]),
        seats=random.choice([2, 3, 4, 20]),
        carClass=random.choice(["A", "B", "C", "D"]),
        pricePerDay=round(random.uniform(30, 300), 2),
        city="Rehovot",
        about=fake.text()[:30],
    )


@pytest.fixture(scope="function")
def auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


