from configparser import ConfigParser
from pathlib import Path

class Config(ConfigParser):
    def __init__(self, path: str = "config.ini", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.read(path)

    def username(self):
        return self["POST"].get("Username")

    def password(self):
        return self["POST"].get("Password")