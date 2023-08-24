from typing import Optional, Dict
from http.client import HTTPResponse
from http.cookies import SimpleCookie
from random import SystemRandom

import urllib.parse
import urllib.error
import hashlib
import re
import json

from .http import HTTPRequest
from .parser import FormParser

HOME_URL = "https://www.post.at/"
LOGIN_INIT_URL = "https://www.post.at/identity/externallogin?authenticationType=post.azureADB2C&ReturnUrl=%2fidentity%2fexternallogincallback%3fReturnUrl%3dhttps%253a%252f%252fwww.post.at%252fen%26sc_site%3dPostAT%26authenticationSource%3dDefault&sc_site=PostAT"
LOGIN_SELF_ASSERTED = "https://login.post.at%(tenant)s/SelfAsserted"
LOGIN_CONFIRMED = "https://login.post.at%(tenant)s/api/%(api)s/confirmed"
OAUTH_BASE = "https://login.post.at/%(tenant)s/%(api)s/oauth2/v2.0"
TOKEN = OAUTH_BASE + "token"
AUTHORIZE = OAUTH_BASE + "authorize"
GRAPHQL_AUTHENTICATED = "https://api.post.at/sendungen/sv/graphqlAuthenticated"
GRAPHQL_PUBLIC = "https://api.post.at/sendungen/sv/graphqlPublic"


class PostAPI:
    """ A class providing a pseudo-API for the Austrian Post website. """

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, login: bool = True):
        """ Initialize the connection to the Austrian Post website.

        Parameters:
            username: The username to use for login (optional)
            password: The password to use for login (optional)
            login: Whether to login immediately or not (default: True, only works if username and password are provided)
        """

        # Initialize variables

        self.cookies: Dict[str, str] = {}
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.login_data: Optional[dict] = None
        self.login_settings: Optional[dict] = None
        self.login_params: Optional[dict] = None

        # Login if credentials are provided and login is enabled

        if username and password:
            self.username = username
            self.password = password

            if login:
                self.login()

    def update_cookies(self, response: HTTPResponse):
        """ Update the cookies from the given response.

        Parameters:
            response: The HTTPResponse object to update the cookies from
        """

        # Get the Set-Cookie header and parse it

        set_cookie_header = response.getheader("Set-Cookie")
        if set_cookie_header:
            cookies = SimpleCookie()

            # Split the header by comma and load the individual cookies

            for cookie in set_cookie_header.split(","):
                cookies.load(cookie.strip())

            # Update the cookies

            for value in cookies.values():
                self.cookies[value.key] = value.value

    def request(self, *args, **kwargs) -> HTTPRequest:
        """ Create a new HTTPRequest with the current cookies.

        Returns:
            The new HTTPRequest
        """

        req = HTTPRequest(*args, **kwargs)
        req.cookies = self.cookies
        return req

    def login(self) -> bool:
        """ Login to the Austrian Post website.

        As there are no public APIs for the Austrian Post website, this method
        basically just emulates a browser login.

        Returns:
            True if the login was successful, False otherwise
        """

        assert self.username and self.password, "Username and password must be provided"

        # Get the home page and update the cookies
        # Not sure if this is necessary, but it doesn't hurt

        # TODO: Fetch the login URL from the home page

        home_req = self.request(HOME_URL)
        home_res = home_req.open()

        self.update_cookies(home_res)

        # Get the login page and update the cookies
        # This is a POST request for some reason

        login_req = self.request(LOGIN_INIT_URL, method="POST")
        login_res = login_req.open()

        self.update_cookies(login_res)

        # The previous request redirects to the actual login page
        # Get the URL and parse the query parameters

        login_url_parts = urllib.parse.urlsplit(login_res.geturl())
        self.login_params = login_params = urllib.parse.parse_qs(
            login_url_parts.query)

        # Generate a code verifier and code challenge
        # The code verifier is a random string of 32 bytes
        # The code challenge is the SHA256 hash of the code verifier
        # This is used for PKCE for the token request

        self.code_verifier = SystemRandom().getrandbits(256).to_bytes(32, "big").hex()
        code_challenge = hashlib.sha256(
            self.code_verifier.encode()).digest().hex()
        login_params["code_challenge"] = code_challenge

        # Reconstruct the login URL

        login_url = urllib.parse.urlunsplit((login_url_parts.scheme, login_url_parts.netloc,
                                            login_url_parts.path, urllib.parse.urlencode(login_params), login_url_parts.fragment))

        # Get the settings from the login page

        login_html = login_res.read().decode()

        login_settings_regex = re.compile(
            r'var SETTINGS = ({.*?});', re.DOTALL)
        login_settings_match = login_settings_regex.search(login_html)
        self.login_settings = login_settings = json.loads(
            login_settings_match.group(1))

        # Get required parameters from the settings

        transaction_id = login_settings["transId"]
        policy = login_settings["hosts"]["policy"]
        tenant = login_settings["hosts"]["tenant"]
        csrf = login_settings["csrf"]
        api = login_settings["api"]

        # Prepare the parameters for the self-asserted login

        self_asserted_params = {
            "tx": transaction_id,
            "p": policy,
        }

        # Get the self-asserted login URL

        self_asserted_url = LOGIN_SELF_ASSERTED % {"tenant": tenant}
        self_asserted_query = urllib.parse.urlencode(self_asserted_params)

        # Encode the payload for the self-asserted login

        self_asserted_payload = urllib.parse.urlencode({
            "request_type": "RESPONSE",
            "signInName": self.username,
            "password": self.password,
        }).encode()

        self_asserted_req = self.request(
            f"{self_asserted_url}?{self_asserted_query}", data=self_asserted_payload, method="POST")

        # Add required headers for the self-asserted login

        self_asserted_req.add_header(
            "Content-Type", "application/x-www-form-urlencoded")
        self_asserted_req.add_header("X-CSRF-TOKEN", csrf)
        self_asserted_req.add_header("X-Requested-With", "XMLHttpRequest")

        # Perform the self-asserted login

        self_asserted_res = self_asserted_req.open()
        self_asserted_response = json.loads(self_asserted_res.read().decode())

        # Check if the login was successful

        if self_asserted_response["status"] != "200":
            return False

        # Update the cookies

        self.update_cookies(self_asserted_res)

        # Prepare the parameters for the confirmation page

        confirmation_params = {
            "rememberMe": "false",
            "csrf_token": csrf,
            "tx": transaction_id,
            "p": policy,
        }

        # Prepare the URL for the confirmation page

        confirmation_url = LOGIN_CONFIRMED % {
            "tenant": tenant, "api": api} + f"?{urllib.parse.urlencode(confirmation_params)}"

        # Get the confirmation page and update the cookies

        confirmation_req = self.request(confirmation_url)

        confirmation_res = confirmation_req.open()

        self.update_cookies(confirmation_res)

        # Use FormParser to parse the confirmation page

        confirmation_html = confirmation_res.read().decode()

        confirmation_parser = FormParser()
        confirmation_parser.feed(confirmation_html)

        # Get the form data from the confirmation page

        form_action = confirmation_parser.form_action
        form_data = confirmation_parser.form_fields

        # Check if the server returned an error

        if "error" in form_data.keys():
            print(form_data["error_description"])
            return False

        # Prepare the final request

        final_url = form_action
        final_payload = urllib.parse.urlencode(form_data).encode()

        final_req = self.request(final_url, data=final_payload, method="POST")

        # Add required headers for the final request

        final_req.add_header(
            "Content-Type", "application/x-www-form-urlencoded")

        # Perform the final request and update the cookies

        final_res = final_req.open()
        self.update_cookies(final_res)

        # Store the login data

        self.login_data = form_data

        # If we got this far, the login was hopefully successful

        return self.logged_in()

    def logged_in(self) -> bool:
        '''Check if the user is logged in

        TODO: Actually verify the login status instead of just checking if login_data is set

        Returns:
            bool: True if the user is logged in, False otherwise
        '''
        return bool(self.login_data)

    def get_token(self) -> str:
        '''Exchange the id_token for an access_token

        Currently not working – may be replaced by more specific methods

        Returns:
            str: The access_token
        '''

        # Assert that the user is logged in

        if not self.logged_in():
            raise Exception("Not authenticated.")

        # Prepare the request

        token_req = self.request(TOKEN, method="POST")
        token_req.add_header(
            "Content-Type", "application/x-www-form-urlencoded")

        # Prepare the payload

        print(self.login_data)

        token_payload = {
            # TODO: Get this from somewhere dynamically
            "client_id": "e2cfcb2a-7dc8-4110-ac2a-9647dd095d9e",
            # TODO: Get this from somewhere dynamically if required
            "redirect_uri": "https://services.post.at",
            # TODO: Get this from somewhere dynamically if required
            "scope": "openid profile offline_access",
            "code": self.login_data["code"],  # TODO: Is this correct?
            "code_verifier": self.code_verifier,
            # TODO: Get this from somewhere dynamically if required
            "grant_type": "authorization_code",
            "client_info": 1,  # TODO: Get this from somewhere dynamically if required
            # TODO: Get this from somewhere dynamically...
            "client-request-id": "706a9572-5395-4e05-9d80-9317491696d6",
        }

        # Perform the request

        token_req.data = urllib.parse.urlencode(token_payload).encode()
        token_res = token_req.open()

        # Parse the response

        token_response = json.loads(token_res.read().decode())

        # For now, just print the response

        print(token_response)

        return ""  # TODO: Actually return the access_token

    def get_shipments_token(self):

        if not self.logged_in():
            raise Exception("Not authenticated.")

        # Prepare the request

        authorize_url = AUTHORIZE % (
            self.login_settings["hosts"]["tenant"], self.login_settings["api"])

        print(authorize_url)

        token_req = self.request(authorize_url, method="GET")

        # Prepare the query string

        token_payload = {
            "response_type": "token",
            "scope": "https://login.post.at/sendungenapi-prod/Sendungen.All openid profile",
            "client_id": self.login_params["client_id"],
            "redirect_uri": self.login_params["redirect_uri"],
            "state": self.login_params["state"],
            "nonce": self.login_params["nonce"],
        }



    def get_shipments(self):
        if not self.logged_in():
            raise Exception("Not authenticated.")

        query = {
            "query": """query
                { sendungen: sendungen(
                    tagFilter: \"Empfangen\"
                    postProcessingOptions : {elementCount: 2}
                )
                { sendungen {
                    sendungsnummer
                    estimatedDelivery {
                        startDate
                        endDate
                        startTime
                        endTime
                        }
                    sender
                    status
                    bezeichnung
                    sendungsEvents {
                        status
                        timestamp
                        reasontypecode
                        }
                    customsInformation {
                        customsDocumentAvailable
                        userDocumentNeeded
                        }
                    }
                }
            }"""
        }

        req = self.request(GRAPHQL_AUTHENTICATED,
                           data=json.dumps(query).encode())
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.id_token}")

        res = req.open()
        return json.loads(res.read().decode())

    def get_shipment_status_public(self, tracking_number):
        req = self.request(GRAPHQL_PUBLIC)

        query = {
            "query": """query {
                einzelsendung(sendungsnummer: \"%s\") {
                    sendungsnummer
                    branchkey
                    estimatedDelivery {
                        startDate
                        endDate
                        startTime
                        endTime
                        }
                    dimensions {
                        height
                        width
                        length
                        }
                    status
                    weight
                    sendungsEvents {
                        timestamp
                        status
                        reasontypecode
                        text
                        textEn
                        eventpostalcode
                        eventcountry
                        }
                    customsInformation {
                        customsDocumentAvailable,
                        userDocumentNeeded
                        }
                    }
                }""" % tracking_number
            }

        req.add_json_payload(query)

        res = req.open()
        return json.loads(res.read().decode())

    def get_shipment_status(self, tracking_number):
        if self.logged_in():
            # TODO: Implement function using graphqlAuthenticated
            pass

        return self.get_shipment_status_public(tracking_number)