import logging
from flask import Flask, request

from migration_orch_core.config import Configuration
from migration_orch_core.rest_api.api import root_blueprint
from migration_orch_core.rest_api.resources.migration import api as migration_api

conf = Configuration()

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'

if conf.LOG_LEVEL == "INFO":
    log_level = logging.INFO
elif conf.LOG_LEVEL == "WARNING":
    log_level = logging.WARNING
else:
    log_level = logging.DEBUG

if conf.LOG_FILE is not None:
    logging.basicConfig(filename=conf.LOG_FILE, level=log_level, format=log_format, datefmt=log_date_format)
else:
    logging.basicConfig(level=log_level, format=log_format, datefmt=log_date_format)

# Rest application
if migration_api is not None:
    app = Flask(__name__)
    app.register_blueprint(root_blueprint)
    logging.info("Flask Successfully started")


    @app.after_request
    def after_request(response):
        if request.full_path.startswith("/v1"):
            logging.debug("'%s' '%s' '%s' '%s' '%s' " % (
            request.remote_addr, request.method, request.scheme, request.full_path, response.status))
        return response

print("FROG4 Migration Orchestrator started")

"""
if __name__ == "__main__":

    logging.info("frog4-migration-orch started...")

    mainController = MainController()
    graphs_path = Configuration().GRAPHS_PATH

    token = None
    graph_id = None

    print("1] Deploy a graph")
    print("2] Migrate graph to another domain")
    print("3] Migrate status")
    print("4] Delete old graph")
    print("0] Reset")
    print("9] Exit")

    while True:

        cmd = input("Choose action: ")

        if cmd == "1":
            try:
                token = mainController.login(Configuration().USERNAME, Configuration.PASSWORD)
            except LoginError as err:
                logging.error(err)

        if cmd == "2":
            nffg_json = dump_json_file(graphs_path+"/graph1.json")
            try:
                graph_id = mainController.deploy_graph(token, nffg_json)
            except Exception as err:
                logging.error(err)

        if cmd == "3":
            nffg_json = dump_json_file(graphs_path + "/graph1.json")
            try:
                graph_id = mainController.migrate_nf(token, graph_id, nffg_json)
            except Exception as err:
                logging.error(err)

        if cmd == "4":
            mainController.migrate_status(Configuration().FROM_VNF_ID, Configuration().TO_VNF_ID)

        if cmd == "5":
            nffg_json = dump_json_file(graphs_path + "/graph1.json")
            mainController.delete_old_nf(graph_id, nffg_json)

        if cmd == "0":
            mainController.reset()

        if cmd == "9":
            break

        else:
            print("Error, invalid command")

    logging.info("frog4-migration-orch stopped!")
"""

