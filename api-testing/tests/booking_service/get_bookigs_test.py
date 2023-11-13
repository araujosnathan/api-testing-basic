from datetime import datetime, timedelta
import pytest
import requests
from jsonschema import validate
from tests.commom_schemas.error_schema import error_schema
from schemas.empty_bookings import empty_bookings
from schemas.all_bookings_schema import all_bookings_schema
from utils.BookingPayloadBuilder import BookingPayloadBuilder
from utils.Utils import Utils


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute the tests of Get Bookings Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def get_bookings(setup, params=None):
    try:
        response = requests.get(
            f"{setup['data']['bookingServiceBaseUrl']}", params=params, timeout=30
        )
        return response
    except (requests.exceptions.RequestException,) as exception:
        pytest.fail(f"Error when getting Bookings: {exception}")


def test_successful_getting_all_booking_users(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])
    body_payload = BookingPayloadBuilder().with_user_id(user_id).build()
    Utils().create_booking(setup, body_payload)

    # Act
    response = get_bookings(setup)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()
    # Check Schema Reponse
    validate(instance=response_json, schema=all_bookings_schema)


def test_successful_getting_all_booking_specific_user(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])
    body_payload = BookingPayloadBuilder().with_user_id(user_id).build()
    Utils().create_booking(setup, body_payload)
    params = {"user": user_id}

    # Act
    response = get_bookings(setup, params)

    # Assert
    assert response.status_code == 200
    response_json = response.json()

    # Check Schema Reponse
    validate(instance=response_json, schema=all_bookings_schema)


def test_getting_empty_bookings_when_user_dont_has_bookings(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])
    params = {"user": user_id}

    # Act
    response = get_bookings(setup, params)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()
    # Check Schema Reponse
    validate(instance=response_json, schema=empty_bookings)


def test_getting_empty_bookings_when_user_has_not_bookings_in_specific_date(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])
    params = {"user": user_id, "date": "2023-11-01"}

    # Act
    response = get_bookings(setup, params)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()
    # Check Schema Reponse
    validate(instance=response_json, schema=empty_bookings)


def test_gettings_bookings_specific_date_of_user(setup):
    # Arrange
    current_date = datetime.now().date().replace(day=1) + timedelta(days=32)
    formatted_date = current_date.strftime("%Y-%m-%d")
    user_id = Utils().create_user(setup["data"])
    body_payload = (
        BookingPayloadBuilder().with_date(formatted_date).with_user_id(user_id).build()
    )

    Utils().create_booking(setup, body_payload)
    params = {"user": user_id, "date": formatted_date}

    # Act
    response = get_bookings(setup, params)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()
    for booking in response_json:
        # Assert that the date value matches the expected value for each response
        assert booking["date"] == formatted_date
        assert booking["userId"] == user_id

    # Check Schema Reponse
    validate(instance=response_json, schema=all_bookings_schema)


def test_gettings_bookings_from_all_users_of_specific_date(setup):
    # Arrange
    current_date = datetime.now().date().replace(day=1) + timedelta(days=32)
    formatted_date = current_date.strftime("%Y-%m-%d")
    for i in range(3):
        user_id = Utils().create_user(setup["data"])
        body_payload = (
            BookingPayloadBuilder()
            .with_date(formatted_date)
            .with_user_id(user_id)
            .build()
        )
        Utils().create_booking(setup, body_payload)
    params = {"date": formatted_date}

    # Act
    response = get_bookings(setup, params)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()

    assert response_json[0]["date"] == formatted_date

    # Check Schema Reponse
    validate(instance=response_json, schema=empty_bookings)


def test_getting_error_user_dont_exist(setup):
    # Arrange
    userId = 9999
    params = {"user": userId}

    # Act
    response = get_bookings(setup, params)

    # Arrange
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("erros") is None
    assert response_json.get("message") == f"No user with id {userId}"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)
