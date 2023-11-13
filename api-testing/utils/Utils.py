import json
import uuid
from faker import Faker
import pytest
import requests

fake = Faker()


class Utils:
    def create_user(self, data):
        body_payload = {
            "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
            "name": fake.first_name(),
            "surname": fake.last_name(),
        }
        try:
            response = requests.post(
                data["userServiceBaseUrl"], json=body_payload, timeout=30
            )
            assert response.status_code == 201
            return response.json().get("id")

        except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
        ) as exception:
            pytest.fail(f"Error when creating User: {exception}")

    def create_booking(self, setup, body_payload):
        try:
            response = requests.post(
                setup["data"]["bookingServiceBaseUrl"],
                json=body_payload,
                timeout=30,
            )
            return response
        except (requests.exceptions.RequestException,) as exception:
            pytest.fail(f"Error when creating Booking: {exception}")
