import pytest
from jsonschema import validate
from utils.BookingPayloadBuilder import BookingPayloadBuilder
from utils.Utils import Utils
from tests.booking_service.schemas.booking_schema import booking_schema
from tests.commom_schemas.error_schema import error_schema

destination_scenarios = ["", "LH", "LGHF", "DUB", "DUB", "DUB"]
origin_scenarios = ["DUB", "DUB", "DUB", "", "LH", "LGHF"]

# List of fields to exclude in each test
excluded_fields = ["date", "destination", "origin", "userId"]

# Expected error messages for each excluded field
expected_error_messages = {
    "date": "must have required property 'date'",
    "destination": "must have required property 'destination'",
    "origin": "must have required property 'origin'",
    "userId": "must have required property 'userId'",
}


# Function to generate the body payload with a specified excluded field
def generate_body_payload(excluded_field):
    body_payload = BookingPayloadBuilder().build()
    if excluded_field in body_payload:
        del body_payload[excluded_field]
    return body_payload


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute tests of Create Booking Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def test_successful_create_booking(setup):
    # Arrange
    userId = Utils().create_user(setup["data"])
    body_payload = BookingPayloadBuilder().with_user_id(userId).build()

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Assert
    assert response.status_code == 201
    response_json = response.json()
    for key, value in body_payload.items():
        assert response_json.get(key) == value, f"Invalid {key} expected"
    validate(instance=response_json, schema=booking_schema)


def test_should_not_create_booking_with_incorrect_date(setup):
    # Arrange
    body_payload = BookingPayloadBuilder().with_wrong_format_date().build()

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert (
        response_json.get("errors", [{}])[0].get("message")
        == 'must match format "date"'
    )
    assert response_json.get("message") == "Validation errors"
    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


def test_should_not_create_booking_with_incorrect_userId_format_type(setup):
    # Arrange
    body_payload = BookingPayloadBuilder().with_user_id("9").build()

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("errors", [{}])[0].get("message") == "must be number"
    assert response_json.get("message") == "Validation errors"
    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


@pytest.mark.parametrize(
    "destination, origin", zip(destination_scenarios, origin_scenarios)
)
def test_should_not_create_booking_with_destination_origin_code_fewer_than_limit_3(
    setup, destination, origin
):
    # Arrange
    body_payload = (
        BookingPayloadBuilder()
        .with_destination(destination)
        .with_origin(origin)
        .build()
    )

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert (
        response_json.get("errors", [{}])[0].get("message")
        == 'must match pattern "^[A-Z]{3}$"'
    )
    assert response_json.get("message") == "Validation errors"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


# Parametrize the test with excluded fields
@pytest.mark.parametrize(
    "excluded_field, expected_error_message",
    zip(excluded_fields, expected_error_messages.values()),
)
def test_shold_not_create_user_with_missing_required_fields(
    setup, excluded_field, expected_error_message
):
    # Arrange
    body_payload = generate_body_payload(excluded_field)

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Arrange
    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("errors", [{}])[0].get("message") == expected_error_message
    assert response_json.get("message") == "Validation errors"
    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)


@pytest.mark.parametrize("destination, origin", [("123", "MAD"), ("MAD", "123")])
def test_should_not_create_booking_with_destination_origin_being_numbers_as_string(
    setup, destination, origin
):
    # Arrange
    body_payload = (
        BookingPayloadBuilder()
        .with_destination(destination)
        .with_origin(origin)
        .build()
    )

    # Act
    response = Utils().create_booking(setup, body_payload)

    # Assert
    assert response.status_code == 400
    response_json = response.json()
    assert (
        response_json.get("errors", [{}])[0].get("message")
        == 'must match pattern "^[A-Z]{3}$"'
    )
    assert response_json.get("message") == "Validation errors"
    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)
