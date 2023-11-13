import uuid
from jsonschema import validate
from behave import *
import requests
from faker import Faker
from tests.user_servive.schemas.specific_user_schema import specific_user_schema
from tests.commom_schemas.error_schema import error_schema

fake = Faker()


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


def create_user(data, body_payload):
    try:
        response = requests.post(
            data["userServiceBaseUrl"],
            json=body_payload,
            timeout=30,
        )
        return response
    except (requests.exceptions.RequestException,) as exception:
        raise Exception(f"Error When Creating User: {exception}")


@given("I have a user to create")
def impl_bk(context):
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": fake.first_name(),
        "surname": fake.last_name(),
    }
    context.user_body_payload = body_payload


@given("I already created an user")
def impl_bk(context):
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": fake.first_name(),
        "surname": fake.last_name(),
    }
    # Act
    response = create_user(context.config.data, body_payload)
    context.user_body_payload = body_payload
    context.user_response = response


@given("I have an user with empty {scenario}")
def step_implpy(context, scenario):
    print(context.config.data)
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": "Name" if scenario == "Surname" else "",
        "surname": "Surnname" if scenario == "Name" else "",
    }
    context.user_body_payload = body_payload


@given('I have an user with minimum character for "{field}"')
def step_implpy(context, field):
    body_payload = {
        "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
        "name": "N" if field == "name" else "Name",
        "surname": "S" if field == "surname" else "Surname",
    }
    context.user_body_payload = body_payload


@given('I have an user with excluded field "{excluded_field}"')
def step_given_user_with_excluded_field(context, excluded_field):
    context.excluded_field = excluded_field
    context.user_body_payload = generate_body_payload(excluded_field)


@when("I call the endoint to create the user")
def impl_bk(context):
    response = create_user(context.config.data, context.user_body_payload)
    context.user_response = response


@then("user should be created with success")
def impl_bk(context):
    assert (
        context.user_response.status_code == 201
    ), f"Expected {200}, but got {context.user_response.status_code}"
    response_json = context.user_response.json()
    assert response_json.get("email") == context.user_body_payload.get(
        "email"
    ), f"Expected {context.user_body_payload.get('email')}, but got {response_json.get('email')}"
    assert response_json.get("name") == context.user_body_payload.get(
        "name"
    ), f"Expected {context.user_body_payload.get('name')}, but got {response_json.get('name')}"
    assert response_json.get("surname") == context.user_body_payload.get(
        "surname"
    ), f"Expected {context.user_body_payload.get('surname')}, but got {response_json.get('surname')}"


@then("user should not be created because aleady exist")
def impl_bk(context):
    assert (
        context.user_response.status_code == 409
    ), f"Expected {409}, but got {context.user_response.status_code}"
    response_json = context.user_response.json()
    assert response_json.get("erros") is None
    assert (
        response_json.get("message")
        == f"User with email '{context.user_body_payload.get('email')}' already exists"
    )


@then("user should not be created because has fewer characters than limit")
def impl_bk(context):
    assert (
        context.user_response.status_code == 400
    ), f"Expected {400}, but got {context.user_response.status_code}"
    response_json = context.user_response.json()
    assert (
        response_json.get("errors", [{}])[0].get("message")
        == "must NOT have fewer than 1 characters"
    )
    assert response_json.get("message") == "Validation errors"


@then('I should receive a validation error message "{expected_error_message}"')
def impl_bk(context, expected_error_message):
    assert (
        context.user_response.status_code == 400
    ), f"Expected {400}, but got {context.user_response.status_code}"
    response_json = context.user_response.json()
    assert response_json.get("errors", [{}])[0].get("message") == expected_error_message
    assert response_json.get("message") == "Validation errors"


@then("the response schema should be the corresponding to the user creation")
def impl_bk(context):
    validate(instance=context.user_response.json(), schema=specific_user_schema)


@then("the response schema should be the corresponding to the error")
def impl_bk(context):
    validate(instance=context.user_response.json(), schema=error_schema)
