import os
from utils.BaseConfig import BaseConfig


# Define a dictionary for environment properties
environment_properties = {}

# Define the Allure directory from the command-line option
alluredir = "allure-results"


def setup(context):
    context.config.setup_logging()
    context.config.define_userdata(
        "env", default="local", description="Environment to use"
    )


def before_all(context):
    ENV = context.config.userdata.get("env")
    DATA = BaseConfig(ENV).load_json_file()
    context.config.data = DATA
    environment_properties["Environment"] = ENV.upper() if ENV else ""
    create_allure_environment_file(context)


# Create the environment.properties file in the Allure directory
def create_allure_environment_file(context):
    global alluredir

    if alluredir and os.path.isdir(alluredir) and environment_properties:
        allure_env_path = os.path.join(alluredir, "environment.properties")

        with open(allure_env_path, "w", encoding="utf-8") as f:
            data = "\n".join(
                [
                    f"{variable}={value}"
                    for variable, value in environment_properties.items()
                ]
            )
            f.write(data)
