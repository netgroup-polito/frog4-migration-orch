from config import Configuration
from requests.exceptions import HTTPError
from exception import LoginError
import requests
import logging
import json

class NffgController():

    def __init__(self):
        orch_address = Configuration().ORCH_ADDRESS
        orch_port = Configuration().ORCH_PORT
        self.base_url = "http://"+str(orch_address)+":"+str(orch_port)
        self.post_url = self.base_url + "/NF-FG/"
        self.put_url = self.base_url + "/NF-FG/%s"
        self.delete_url = self.base_url + "/NF-FG/%s"

        execution = Configuration().EXECUTION
        if execution.__eq__("debug"):
            self.username = Configuration().USERNAME
            self.password = Configuration().PASSWORD
        self.authentication_url = self.base_url + "/login"
        self.token = None

        self.headers = None


    def post(self, nffg_json):
        try:
            if self.token is None:
                self.getToken(self.username, self.password)
            resp = requests.put(self.post_url, data=nffg_json, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                logging.debug("Token expired, getting a new one...")
                self.getToken(self.username, self.password)
                resp = requests.put(self.post_url, data=nffg_json, headers=self.headers)
                resp.raise_for_status()
                return resp.text
            else:
                raise err
        except Exception as ex:
            raise ex

    def update(self, nffg_id, nffg_json):
        try:
            if self.token is None:
                self.getToken(self.username, self.password)
            resp = requests.put(self.put_url % (nffg_id), data=nffg_json, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                logging.debug("Token expired, getting a new one...")
                self.getToken(self.username, self.password)
                resp = requests.put(self.put_url % (nffg_id), data=nffg_json, headers=self.headers)
                resp.raise_for_status()
                return resp.text
            else:
                raise err
        except Exception as ex:
            raise ex

    def delete(self, nffg_id):
        try:
            if self.token is None:
                self.getToken(self.username, self.password)
            resp = requests.delete(self.delete_url % (nffg_id), headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            if err.response.status_code == 401:
                logging.debug("Token expired, getting a new one...")
                self.getToken(self.username, self.password)
                resp = requests.delete(self.delete_url % (nffg_id), headers=self.headers)
                resp.raise_for_status()
                return resp.text
            else:
                raise err
        except Exception as ex:
            raise ex

    def getToken(self, username, password):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        authenticationData = {'username': username, 'password': password}
        resp = requests.post(self.authentication_url, data=json.dumps(authenticationData), headers=headers)
        try:
            resp.raise_for_status()
            logging.debug("Authentication successfully performed")
            self.token = resp.text
            self.headers = {'Content-Type': 'application/json',
                'cache-control': 'no-cache',
                'X-Auth-Token': self.token}
        except HTTPError as err:
            logging.error(err)
            raise LoginError("login failed: " + str(err))