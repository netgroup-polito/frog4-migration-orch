import logging
from pprint import pprint
from requests.exceptions import HTTPError

from migration_orch_core.exception.token_expired import TokenExpired
from migration_orch_core.service.graph_service import GraphService
from migration_orch_core.service.authentication_service import AuthenticationService
from migration_orch_core.service.configuration_service import ConfigurationService

class MainController():

    def login(self, username, password):
        """
        Perform login into the frog4-orchestrator
        :param username: 
        :param password: 
        :return: token
        """
        authService = AuthenticationService()
        try:
            logging.debug("Trying to login...")
            token = authService.login(username, password)
            logging.debug("Trying to login...done! Token: " + token)
            return token

        except HTTPError as err:
            logging.error("Trying to login...Error! HTTPError: " + err.message)
            raise err
        except Exception as err:
            logging.error("Trying to login...Error! Exception: " + str(err))
            raise err

    def post_graph(self, token, graph_json):
        graphService = GraphService()
        try:
            logging.debug("Post graph...")
            graph_id = graphService.post_graph(token, graph_json)
            logging.debug("Post graph...done! graph_id = " + graph_id)
            return graph_id

        except TokenExpired as err:
            logging.error("Post graph...Error! TokenExpiredException: " + err.message)
            raise err
        except HTTPError as err:
            logging.error("Post graph...Error! HttpErrorException: " + str(err))
            raise err
        except Exception as err:
            logging.error("Post graph...Error! Exception: " + str(err))
            raise err

    def update_graph(self, token, graph_id, new_graph_json):
        graphService = GraphService()
        try:
            logging.debug("Updating graph " + graph_id +"...")
            graph_id = graphService.update_graph(token, graph_id, new_graph_json)
            logging.debug("Updating graph " + graph_id +"...done!")
            return graph_id

        except TokenExpired as err:
            logging.error("Updating graph " + graph_id +"...Error! TokenExpiredException: " + err.get_mess())
            raise err
        except HTTPError as err:
            logging.error("Updating graph " + graph_id +"...Error! HttpErrorException: " + str(err))
            raise err
        except Exception as err:
            logging.error("Updating graph " + graph_id +"...Error! Exception: " + str(err))
            raise err

    def delete_graph(self, token, graph_id):
        graphService = GraphService()
        try:
            logging.debug(" -> Deleting graph " + graph_id + "...")
            graphService.delete_graph(token, graph_id)
            logging.debug(" -> Deleting graph " + graph_id + "...done!")

        except TokenExpired as err:
            logging.error(" -> Deleting graph " + graph_id + "...Error! TokenExpiredException: " + err.get_mess())
            raise err
        except HTTPError as err:
            logging.error(" -> Deleting graph " + graph_id + "...Error! HttpErrorException: " + str(err))
            raise err
        except Exception as err:
            logging.error(" -> Deleting graph " + graph_id + "...Error! Exception: " + str(err))
            raise err

    def get_status_from_nf(self, tenant_id, graph_id, vnf_id):
        """
        Get the current state from the current network function
        :param tenant_id: 
        :param graph_id: 
        :param vnf_id: 
        :return: status
        """
        configurationService = ConfigurationService()
        try:
            logging.debug(" -> Getting status from old network function...")
            json_status = configurationService.get_status(tenant_id, graph_id, vnf_id)
            logging.debug(" -> Getting status from old network function...Done! Status:")
            pprint(json_status)

        except HTTPError as err:
            logging.error(" -> Getting status from old network function...Error! HttpErrorException: " + str(err))
            raise err
        except Exception as err:
            logging.error(" -> Getting status from old network function...Error! Exception: " + str(err))
            logging.debug("Migrating status...Error!")
            raise err

    def push_status_into_nf(self, tenant_id, graph_id, vnf_id, json_status):
        """
        Push the status into the network function
        :param tenant_id: 
        :param graph_id: 
        :param vnf_id: 
        :return: 
        """
        configurationService = ConfigurationService()
        try:
            logging.debug(" -> Pushing status into new network function...")
            configurationService.push_status(tenant_id, graph_id, vnf_id, json_status)
            logging.debug(" -> Pushing status into new network function...Done!")

        except HTTPError as err:
            logging.error(" -> Pushing status from old network function...Error! HttpErrorException: " + str(err))
            raise err
        except Exception as err:
            logging.error(" -> Pushing status from old network function...Error! Exception: " + str(err))
            logging.debug("Migrating status...Error!")
            raise err



