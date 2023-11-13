import pytest
import requests
from jsonschema import validate
from tests.commom_schemas.error_schema import error_schema
from schemas.booking_schema import booking_schema
from utils.BookingPayloadBuilder import BookingPayloadBuilder
from utils.Utils import Utils


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute the tests of Get Specific Booking Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def get_booking_id(setup, booking_id):
    try:
        response = requests.get(
            f"{setup['data']['bookingServiceBaseUrl']}/{booking_id}", timeout=30
        )
        return response
    except (requests.exceptions.RequestException,) as exception:
        pytest.fail(f"Error When Getting Booking: {exception}")


def test_successful_getting_booking_specific_id(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])
    body_payload = BookingPayloadBuilder().with_user_id(user_id).build()
    bookig_id = Utils().create_booking(setup, body_payload).json().get("id")

    # Act
    response = get_booking_id(setup, bookig_id)

    # Arrange
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == bookig_id

    # Check Schema Reponse
    validate(instance=response_json, schema=booking_schema)


def test_getting_booking_not_exist(setup):
    # Arrange
    bookingId = 99999999999

    # Act
    response = get_booking_id(setup, bookingId)

    # Arrange
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("erros") is None
    assert response_json.get("message") == f"No booking with id {bookingId}"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)
