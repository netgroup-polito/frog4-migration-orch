from config import Configuration
from requests.exceptions import HTTPError
import requests
import logging
import json

class StatusController():

    def __init__(self):
        self.base_url = Configuration().CONFIGURATION_ORCH_URL

        self.headers = {'Content-Type': 'application/json'}

    def get_status(self):
        try:
            resp = requests.get(self.get_status_url, headers=self.headers)
            resp.raise_for_status()
            return json.loads(resp.text)
        except HTTPError as err:
            raise err

    def push_status(self, json_status):
        try:
            resp = requests.put(self.push_status_url, data=json_status, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            raise err