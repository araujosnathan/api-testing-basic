import json
from os.path import join, dirname


class BaseConfig:
    def __init__(self, env):
        self.env = env
        self.data = self.load_json_file()

    def load_json_file(self):
        absolute_path = join(dirname(__file__), f"data_{self.env}.json")

        with open(absolute_path, encoding="utf-8") as read_file:
            data = json.loads(read_file.read())

        return data
