from flask import Blueprint
from flask_restplus import Api

root_blueprint = Blueprint('root', __name__)
api = Api(root_blueprint, version='1.0', title='Migration Orchestrator API', description='Migration Orchestrator API',
          doc='/api_docs/')