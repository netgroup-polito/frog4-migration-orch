from config_parser import ConfigParser
from requests.exceptions import HTTPError
import requests
import logging
import json

class StatusController():

    def __init__(self):
        self.configParser = ConfigParser()

        src_address = self.configParser.get("from_vnf", "address")
        src_port = self.configParser.get("from_vnf", "port")
        src_base_url = "http://" + str(src_address) + ":" + str(src_port)
        self.get_status_url = src_base_url + str(self.configParser.get("from_vnf", "get_status_url"))

        dst_address = self.configParser.get("to_vnf", "address")
        dst_port = self.configParser.get("to_vnf", "port")
        dst_base_url = "http://" + str(dst_address) + ":" + str(dst_port)
        self.push_status_url = dst_base_url + str(self.configParser.get("to_vnf", "push_status_url"))

        self.headers = {'Content-Type': 'application/json'}

    def get_status(self):
        try:
            resp = requests.get(self.get_status_url, headers=self.headers)
            resp.raise_for_status()
            return json.loads(resp.text)
        except HTTPError as err:
            logging.debug("Getting status from old network function...Error!")
            raise err

    def push_status(self, json_status):
        try:
            resp = requests.put(self.push_status_url, data=json_status, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            logging.debug("Pushing status into new network function...Error!")
            raise err