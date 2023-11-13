import pytest
import requests
from jsonschema import validate
from tests.user_servive.schemas.specific_user_schema import specific_user_schema
from tests.commom_schemas.error_schema import error_schema
from utils.Utils import Utils


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute the tests of Get Specifics User Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def test_successful_getting_specific_user(setup):
    # Arrange
    user_id = Utils().create_user(setup["data"])

    # Act
    response = requests.get(
        f"{setup['data']['userServiceBaseUrl']}/{user_id}", timeout=30
    )

    # Assert
    assert response.status_code == 200
    response_json = response.json()

    # Check Schema Reponse
    validate(instance=response_json, schema=specific_user_schema)


def test_getting_user_not_exist(setup):
    # Arrange
    userId = 999

    # Act
    response = requests.get(
        f"{setup['data']['userServiceBaseUrl']}/{userId}", timeout=30
    )

    # Assert
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("erros") is None
    assert response_json.get("message") == f"No user with id {userId}"

    # Check Schema Reponse
    validate(instance=response_json, schema=error_schema)
