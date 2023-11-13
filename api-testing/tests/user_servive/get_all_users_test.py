import pytest
import requests
from jsonschema import validate
from tests.user_servive.schemas.all_users_schema import all_users_schema
from utils.Utils import Utils


@pytest.fixture(name="setup")
def setup_fixture(get_data):
    """Init Configuration to execute the tests of Get All Users Endpoint
    :get_data is a function initialized in conftest.py to be used for all file tests
    """
    yield {
        "data": get_data,
    }


def test_successful_getting_all_users(setup):
    # Arrange
    Utils().create_user(setup["data"])

    # Act
    response = requests.get(setup["data"]["userServiceBaseUrl"], timeout=30)

    # Assert
    assert response.status_code == 200
    response_json = response.json()

    # Check Schema Reponse
    validate(instance=response_json, schema=all_users_schema)
