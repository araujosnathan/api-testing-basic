"""Class to get the environment to run the tests and other commom functions"""


from os import path
from pytest import fixture
from utils.BaseConfig import BaseConfig


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="local", help="Environment to run the tests"
    )


@fixture(scope="session", autouse=True)
def build_allure_environment_properties(request):
    environment_properties = {}

    environment_properties.update(
        {"Environment": request.config.getoption("--env").upper()}
    )

    alluredir = request.config.getoption("--alluredir")

    if not alluredir or not path.isdir(alluredir) or not environment_properties:
        return

    allure_env_path = path.join(alluredir, "environment.properties")

    with open(allure_env_path, "w", encoding="utf-8") as _f:
        data = "\n".join(
            [
                f"{variable}={value}"
                for variable, value in environment_properties.items()
            ]
        )
        _f.write(data)


@fixture(scope="session")
def get_data(request):
    """Init Configuration to get DATA"""

    ENV = request.config.getoption("--env")
    DATA = BaseConfig(ENV).load_json_file()
    return DATA
