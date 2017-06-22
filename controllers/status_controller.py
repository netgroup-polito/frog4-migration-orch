from config import Configuration
from requests.exceptions import HTTPError
import requests
import logging
import json

class StatusController():

    def __init__(self):
        self.base_url = Configuration().CONFIGURATION_ORCH_URL
        self.headers = {'Content-Type': 'application/json'}

    def get_status(self, tenant_id, graph_id, vnf_id):
        get_status_url = self.base_url + '/' + tenant_id + '/' + graph_id + '/' + vnf_id + '/'
        try:
            resp = requests.get(get_status_url, headers=self.headers)
            resp.raise_for_status()
            return json.loads(resp.text)
        except HTTPError as err:
            raise err

    def push_status(self, tenant_id, graph_id, vnf_id, json_status):
        push_status_url = self.base_url + '/' + tenant_id + '/' + graph_id + '/' + vnf_id + '/'
        try:
            resp = requests.put(push_status_url, data=json_status, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            raise err