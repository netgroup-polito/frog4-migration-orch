from config_parser import ConfigParser
from controllers.nffg_controller import NffgController
from controllers.status_controller import StatusController
from requests.exceptions import HTTPError
from pprint import pprint

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class Controller():

    def __init__(self):

        self.configParser = ConfigParser()
        self.statusController = StatusController()
        self.nffgController = NffgController()

        self.tenant_id = self.configParser.get("nffg_params", "tenant_id")
        self.graph_id = self.configParser.get("nffg_params", "graph_id")
        self.vnf_id = self.configParser.get("nffg_params", "vnf_id")

        self._start()


    def _start(self):
        logging.info("frog4-migration-orch started...")

        print("1] Deploy a graph")
        print("2] Migrate graph to another domain")
        print("3] Migrate status")
        print("4] Delete old graph")
        print("0] Reset")
        print("9] Exit")

        while True:
            cmd = input("Choose action: ")
            if cmd == "1":
                self._deploy_graph()
            if cmd == "2":
                self._migrate_nf()
            if cmd == "3":
                self._migrate_status()
            if cmd == "4":
                self._delete_old_nf()
            if cmd == "0":
                self._reset()
            if cmd == "9":
                break
            else:
                print("Error, invalid command")

        logging.info("frog4-migration-orch stopped...")


    def _deploy_graph(self):
        try:
            logging.debug("Deploying graph...")
            nffg_json = self.dump_json_file("graphs/graph1.json")
            self.graph_id = self.nffgController.post(nffg_json)
            logging.debug("Deploying graph...done! graph_id = " + self.graph_id)
        except Exception as ex:
            logging.error("Deploying graph...Error!")
            logging.error(ex)

    def _migrate_nf(self):
        try:
            logging.debug("Migrate network function...")
            nffg_json = self.dump_json_file("graphs/graph2.json")
            self.graph_id = self.nffgController.update(self.graph_id, nffg_json)
            logging.debug("Migrate network function...done!")
        except Exception as ex:
            logging.error("Migrate network function...Error!")
            logging.error(ex)
            self._reset()

    def _migrate_status(self):
        try:
            logging.debug("Getting status from old network function...")
            json_status = self.statusController.get_status()
            logging.debug("Getting status from old network function...Done! Status:")
            pprint(json_status)
            logging.debug("Pushing status into new network function...")
            self.statusController.push_status(json_status)
            logging.debug("Pushing status into new network function...Done!")
        except Exception as ex:
            logging.error(ex)
            self._reset()

    def _delete_old_nf(self):
        try:
            logging.debug("Delete old network function...")
            nffg_json = self.dump_json_file("graphs/graph3.json")
            self.graph_id = self.nffgController.update(self.graph_id, nffg_json)
            logging.debug("Delete old network function...done!")
        except Exception as ex:
            logging.error("Delete old network function...Error!")
            logging.error(ex)
            self._reset()

    def _reset(self):
        if self.graph_id is not None:
            logging.debug("Reset all...")
            try:
                logging.debug(" -> Deleting graph with id: " + self.graph_id + "...")
                self.nffgController.delete(self.graph_id)
                logging.debug(" -> Deleting graph with id: " + self.graph_id + "...done!")
            except Exception as ex:
                logging.debug("Reset all...Error!")
                logging.error(" -> Deleting graph with id: " + self.graph_id + "...Error!")
                logging.error(ex)
            logging.debug("Reset all...done!")


    def dump_json_file(self, filepath):
        try:
            with open(filepath) as file:
                json_data = file.read()
            file.close
            return json_data
        except Exception as ex:
            raise IOError(str(ex))
