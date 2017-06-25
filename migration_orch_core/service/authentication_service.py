from requests.exceptions import HTTPError
from migration_orch_core.config import Configuration
from migration_orch_core.exception.login_error import LoginError

import requests
import logging
import json

class AuthenticationService():

    def __init__(self):
        self.base_url = Configuration().GLOBAL_ORCH_URL

    def login(self, username, password):
        login_url = self.base_url + "/login"
        authentication_data = {'username': username, 'password': password}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            resp = requests.post(login_url, data=json.dumps(authentication_data), headers=headers)
            resp.raise_for_status()
            token = resp.text
            return token
        except HTTPError as err:
            raise err