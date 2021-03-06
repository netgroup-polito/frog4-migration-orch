import json
from requests.exceptions import HTTPError

from flask import request, Response, send_from_directory
from flask_restplus import Resource, fields

from migration_orch_core.exception.token_expired import TokenExpired
from migration_orch_core.controller.main_controller import MainController
from migration_orch_core.rest_api.api import api
import logging

root_ns = api.namespace('v1', 'Global Resource')

login_user_model = api.model('Login', {
    'username': fields.String(required=True, description='Username',  type='string'),
    'password': fields.String(required=True, description='Password',  type='string')})
@root_ns.route('/login', methods=['POST'])
class UserLogin(Resource):
    @root_ns.expect(login_user_model)
    @root_ns.response(200, 'Login Successfully')
    @root_ns.response(401, 'Login Failure')
    @root_ns.response(500, 'Internal Error.')
    def post(self):
        mainController = MainController()
        try:
            json_data = json.loads(request.data.decode())
            username = json_data['username']
            password = json_data['password']
            token = mainController.login(username, password)
            resp = {}
            resp['token'] = token
            return Response(json.dumps(resp), status=200, mimetype="application/json")

        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            logging.debug("Exception: " + str(err))
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@root_ns.route('/graphs', methods=['POST'])
@root_ns.route('/graphs/<id>', methods=['PUT', 'DELETE'])
class Graph(Resource):
    @root_ns.param("X-Auth-Token", "Authentication Token", "header", type="string", required=True)
    @root_ns.param("NFFG", "Graph to be deployed", "body", type="string", required=True)
    @root_ns.response(200, 'Ok')
    @root_ns.response(401, 'Unauthorized.')
    @root_ns.response(500, 'Internal Error')
    def post(self):
        mainController = MainController()
        token = request.headers['X-Auth-Token']
        try:
            graph_id = mainController.post_graph(token, request.data.decode())
            resp = {}
            resp['id'] = graph_id
            return Response(json.dumps(resp), status=200, mimetype="application/json")

        except TokenExpired as err:
            return Response(json.dumps(err.get_mess()), status=401, mimetype="application/json")
        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @root_ns.param("X-Auth-Token", "Authentication Token", "header", type="string", required=True)
    @root_ns.response(200, 'Ok')
    @root_ns.response(401, 'Unauthorized.')
    @root_ns.response(404, 'Not Found')
    @root_ns.response(500, 'Internal Error')
    def put(self, id):
        mainController = MainController()
        token = request.headers['X-Auth-Token']
        try:
            graph_id = mainController.update_graph(token, id, request.data.decode())
            resp = {}
            resp['id'] = graph_id
            return Response(json.dumps(resp), status=200, mimetype="application/json")

        except TokenExpired as err:
            return Response(json.dumps(err.get_mess()), status=401, mimetype="application/json")
        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @root_ns.param("X-Auth-Token", "Authentication Token", "header", type="string", required=True)
    @root_ns.response(200, 'Ok')
    @root_ns.response(401, 'Unauthorized.')
    @root_ns.response(404, 'Not Found')
    @root_ns.response(500, 'Internal Error')
    def delete(self, id):
        mainController = MainController()
        token = request.headers['X-Auth-Token']
        try:
            return mainController.delete_graph(token, id)

        except TokenExpired as err:
            return Response(json.dumps(err.get_mess()), status=401, mimetype="application/json")
        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@root_ns.route('/status/<tenant_id>/<graph_id>/<vnf_id>/', methods=['GET', 'PUT'])
class Status(Resource):
    @root_ns.response(200, 'Ok')
    @root_ns.response(404, 'Not Found')
    @root_ns.response(500, 'Internal Error')
    def get(self, tenant_id, graph_id, vnf_id):
        mainController = MainController()
        try:
            return mainController.get_status_from_nf(tenant_id, graph_id, vnf_id)
        
        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @root_ns.param("Status", "Status to push", "body", type="string", required=True)
    @root_ns.response(200, 'Ok')
    @root_ns.response(404, 'Not Found')
    @root_ns.response(500, 'Internal Error')
    def put(self, tenant_id, graph_id, vnf_id):
        mainController = MainController()
        try:
            return mainController.push_status_into_nf(tenant_id, graph_id, vnf_id, request.data.decode())

        except HTTPError as err:
            return Response(json.dumps(str(err)), status=err.response.status_code, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")
