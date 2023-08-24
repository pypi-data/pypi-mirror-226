from urllib.request import Request, urlopen

import json

USER_AGENT = "PostAT/dev (https://kumig.it/kumitterer/postat.git)"

class HTTPRequest(Request):
    def build_cookie_header(self):
        cookiestrings = [f"{name}={value}" for name, value in self.cookies.items()]
        return "; ".join(cookiestrings)

    def open(self):
        if self.cookies:
            self.add_header("Cookie", self.build_cookie_header())

        return urlopen(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cookies = dict()
        self.add_header("User-Agent", USER_AGENT)

    def add_json_payload(self, payload: dict|str):
        self.add_header("Content-Type", "application/json")

        if isinstance(payload, dict):
            payload = json.dumps(payload)

        self.data = payload.encode("utf-8")