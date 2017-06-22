from controllers.nffg_controller import NffgController
from controllers.status_controller import StatusController
from requests.exceptions import HTTPError
from exception import LoginError

from pprint import pprint
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class MainController():

    def __init__(self):
        self.statusController = StatusController()
        self.nffgController = NffgController()

        self.tenant_id = None
        self.graph_id = None
        self.from_vnf_id = None
        self.to_vnf_id = None

    def login(self, username, password):
        """
        Perform login into the frog4-orchestrator
        :param username: 
        :param password: 
        :return: token
        """
        try:
            logging.debug("Trying to login...")
            token = self.nffgController.getToken(username, password)
            logging.debug("Trying to login...done!")
            self.tenant_id = username
            return token
        except HTTPError as err:
            logging.error("Trying to login...Error!")
            raise LoginError("login failed: " + str(err))

    def deploy_graph(self, token, nffg_json):
        """
        Deploy the initial graph
        :param nffg_json: initial graph to deploy 
        :return: id of the deployed graph
        """
        try:
            logging.debug("Deploying graph...")
            id = self.nffgController.post(token, nffg_json)
            self.graph_id = id
            logging.debug("Deploying graph...done! graph_id = " + self.graph_id)
            return self.graph_id

        except Exception as ex:
            logging.error("Deploying graph...Error!")
            logging.error(ex)

    def migrate_nf(self, token, id_nffg_to_update, new_nffg_json):
        """
        Update the graph adding the network function in the other domain
        :param old_nffg_id: id of the current deployed graph
        :param new_nffg_json: graph updated
        :return: id of the updated graph
        """
        try:
            logging.debug("Migrating network function...")
            id = self.nffgController.update(token, id_nffg_to_update, new_nffg_json)
            self.graph_id = id
            logging.debug("Migrating network function...done!")
            return self.graph_id
        except Exception as ex:
            logging.error("Migrating network function...Error!")
            logging.error(ex)
            self.reset()

    def migrate_status(self, from_vnf_id, to_vnf_id):
        """
        Get the current state from the current network function
        and push it into the migrated network function
        :return: 
        """
        logging.debug("Migrating status...")
        try:
            logging.debug(" -> Getting status from old network function...")
            json_status = self.statusController.get_status(self.tenant_id, self.graph_id, from_vnf_id)
            logging.debug(" -> Getting status from old network function...Done! Status:")
            pprint(json_status)
        except Exception as ex:
            logging.error(" -> Getting status from old network function...Error!")
            logging.error(ex)
            logging.debug("Migrating status...Error!")
            self.reset()
            return

        try:
            logging.debug(" -> Pushing status into new network function...")
            self.statusController.push_status(self.tenant_id, self.graph_id, to_vnf_id, json_status)
            logging.debug(" -> Pushing status into new network function...Done!")
        except Exception as ex:
            logging.debug(" -> Pushing status into new network function...Error!")
            logging.error(ex)
            logging.debug("Migrating status...Error!")
            self.reset()
        logging.debug("Migrating status...done!")

    def delete_old_nf(self, token, id_nffg_to_update, new_nffg_json):
        """
        Update the graph, removing the old network function
        :param old_nffg_id: id of the current deployed graph
        :param new_nffg_json: graph updated
        :return: id of the updated graph
        """
        try:
            logging.debug("Deleting old network function...")
            id = self.nffgController.update(token, id_nffg_to_update, new_nffg_json)
            self.graph_id = id
            logging.debug("Deleting old network function...done!")
        except Exception as ex:
            logging.error("Deleting old network function...Error!")
            logging.error(ex)
            self.reset()

    def reset(self):
        if self.graph_id is None:
            return
        try:
            logging.debug("Reset all...")
            logging.debug(" -> Deleting graph with id: " + self.graph_id + "...")
            self.nffgController.delete(self.graph_id)
            logging.debug(" -> Deleting graph with id: " + self.graph_id + "...done!")
            self.graph_id = None
            logging.debug("Reset all...done!")
        except Exception as ex:
            logging.error(" -> Deleting graph with id: " + self.graph_id + "...Error!")
            logging.error(ex)
            logging.debug("Reset all...Error!")


