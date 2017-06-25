import json
import logging
import requests
from requests.exceptions import HTTPError

from migration_orch_core.exception.token_expired import TokenExpired
from migration_orch_core.config import Configuration


class GraphService():

    def __init__(self):
        self.base_url = Configuration().GLOBAL_ORCH_URL
        self.post_url = self.base_url + "/NF-FG/"
        self.put_url = self.base_url + "/NF-FG/%s"
        self.delete_url = self.base_url + "/NF-FG/%s"


    def post_graph(self, token, nffg_json):
        headers = self._get_headers(token)
        try:
            resp = requests.put(self.post_url, data=nffg_json, headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                raise TokenExpired("Token expired")
            raise err
        except Exception as ex:
            raise ex

    def update_graph(self, token, nffg_id, nffg_json):
        headers = self._get_headers(token)
        try:
            resp = requests.put(self.put_url % (nffg_id), data=nffg_json, headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                raise TokenExpired("Token expired")
            raise err
        except Exception as ex:
            raise ex

    def delete_graph(self, token, nffg_id):
        headers = self._get_headers(token)
        try:
            resp = requests.delete(self.delete_url % (nffg_id), headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                raise TokenExpired("Token expired")
            raise err
        except Exception as ex:
            raise ex


    def _get_headers(self, token):
        headers = {'Content-Type': 'application/json',
                        'cache-control': 'no-cache',
                        'X-Auth-Token': token}
        return headers