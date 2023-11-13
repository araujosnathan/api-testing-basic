import uuid
from faker import Faker
import pytest
import requests
from jsonschema import validate
from tests.user_servive.schemas.specific_user_schema import specific_user_schema
from tests.commom_schemas.error_schema import error_schema

fake = Faker()


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute the tests of Create User Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def create_user(setup, body_payload):
    try:
        response = requests.post(
            setup["data"]["userServiceBaseUrl"],
            json=body_payload,
            timeout=30,
        )
        return response
    except (requests.exceptions.RequestException,) as exception:
        pytest.fail(f"Error When Creating User: {exception}")


def test_successful_create_user(setup):
    # Arrange
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": fake.first_name(),
        "surname": fake.last_name(),
    }

    # Act
    response = create_user(setup, body_payload)

    # Assert
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("email") == body_payload.get("email")
    assert response_json.get("name") == body_payload.get("name")
    assert response_json.get("surname") == body_payload.get("surname")

    # Check Schema Reponse
    validate(instance=response_json, schema=specific_user_schema)


def test_impossible_to_create_user_already_created(setup):
    # Arrange

    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": fake.first_name(),
        "surname": fake.last_name(),
    }
    # Act
    response = create_user(setup, body_payload)
    response = create_user(setup, body_payload)

    # Assert
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("erros") is None
    assert (
        response_json.get("message")
        == f"User with email '{body_payload.get('email')}' already exists"
    )

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


# Function to generate the body payload with a specified excluded field
def generate_body_payload(excluded_field):
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": fake.first_name(),
        "surname": fake.last_name(),
    }
    if excluded_field in body_payload:
        del body_payload[excluded_field]
    return body_payload


# List of fields to exclude in each test
excluded_fields = ["email", "name", "surname"]

# Expected error messages for each excluded field
expected_error_messages = {
    "email": "must have required property 'email'",
    "name": "must have required property 'name'",
    "surname": "must have required property 'surname'",
}


# Parametrize the test with excluded fields
@pytest.mark.parametrize(
    "excluded_field, expected_error_message",
    zip(excluded_fields, expected_error_messages.values()),
)
def test_create_user_with_missing_required_fields(
    setup, excluded_field, expected_error_message
):
    # Arrange
    body_payload = generate_body_payload(excluded_field)

    # Act
    response = create_user(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("errors", [{}])[0].get("message") == expected_error_message
    assert response_json.get("message") == "Validation errors"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


@pytest.mark.parametrize("name, surname", [("", "Surname"), ("Name", "")])
def test_error_when_name_surname_have_fewer_characters_than_limit(setup, name, surname):
    # Arrange
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": name,
        "surname": surname,
    }
    # Act
    response = create_user(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert (
        response_json.get("errors", [{}])[0].get("message")
        == "must NOT have fewer than 1 characters"
    )
    assert response_json.get("message") == "Validation errors"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


@pytest.mark.parametrize("name, surname", [("N", "Surname"), ("Name", "S")])
def test_success_when_name_surname_have_edge_of_limit_characters(setup, name, surname):
    # Arrange
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": name,
        "surname": surname,
    }

    # Act
    response = create_user(setup, body_payload)

    # Assert
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == name
    assert response_json.get("surname") == surname

    # Check Schema Reponse
    validate(instance=response_json, schema=specific_user_schema)
