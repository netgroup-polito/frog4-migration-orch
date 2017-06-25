import json
import requests
from requests.exceptions import HTTPError

from migration_orch_core.config import Configuration

class ConfigurationService():

    def __init__(self):
        self.base_url = Configuration().CONFIGURATION_ORCH_URL

    def get_status(self, tenant_id, graph_id, vnf_id):
        get_status_url = self.base_url + '/' + tenant_id + '/' + graph_id + '/' + vnf_id + '/'
        headers = {'Content-Type': 'application/json'}
        try:
            resp = requests.get(get_status_url, headers=headers)
            resp.raise_for_status()
            return json.loads(resp.text)
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex

    def push_status(self, tenant_id, graph_id, vnf_id, json_status):
        push_status_url = self.base_url + '/' + tenant_id + '/' + graph_id + '/' + vnf_id + '/'
        headers = {'Content-Type': 'application/json'}
        try:
            resp = requests.put(push_status_url, data=json_status, headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex