from postat.classes.api import PostAPI
from postat.classes.config import Config

import unittest

class TestConfig(unittest.TestCase):
    def test_config(self):
        config = Config()
        config.read("config.ini")
        self.assertTrue(config.username())
        self.assertTrue(config.password())

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.read("config.ini")
        self.api = PostAPI(self.config.username(), self.config.password(), False)

    def test_login(self):
        login_status = self.api.login()
        self.assertTrue(self.api.logged_in())

    def test_token(self):
        self.api.login()
        token = self.api.get_token()
        self.assertTrue(token)
