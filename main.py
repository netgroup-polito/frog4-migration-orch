import logging
from flask import Flask, request

from migration_orch_core.config import Configuration
from migration_orch_core.rest_api.api import root_blueprint
from migration_orch_core.rest_api.resources.migration import api as migration_api
from web_gui.gui_blueprint import web_gui

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
    app = Flask(__name__, static_folder = 'web_gui/static')
    app.register_blueprint(root_blueprint)
    app.register_blueprint(web_gui)
    logging.info("Flask Successfully started")


    @app.after_request
    def after_request(response):
        if request.full_path.startswith("/v1"):
            logging.debug("'%s' '%s' '%s' '%s' '%s' " % (
            request.remote_addr, request.method, request.scheme, request.full_path, response.status))
        return response

print("FROG4 Migration Orchestrator started")
