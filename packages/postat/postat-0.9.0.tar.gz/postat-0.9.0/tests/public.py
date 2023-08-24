import unittest

from postat.classes.api import PostAPI

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = PostAPI()

    def test_login(self):
        with self.assertRaises(AssertionError):
            login_status = self.api.login()

        self.assertFalse(self.api.logged_in())

    def test_shipment_status(self):
        tracking_number = "1040906121766650280101"
        shipment_status = self.api.get_shipment_status(tracking_number)
        self.assertEqual(shipment_status["data"]["einzelsendung"]["sendungsnummer"], tracking_number)
        
