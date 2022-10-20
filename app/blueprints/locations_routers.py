# flask
from flask import request, jsonify, Blueprint, Response

# location list
from modules import ZabbixRoutersInventory
from requests.exceptions import ConnectionError
from configs import ZABBIX_SERVER_URL, JSON_LOCATIONS_PATH
from json import dump, load

# response
from . import ERROR_RESPONSE_MESSAGES, ResponseTemplate

# type hints
from typing import Dict

# for logging
import logging

logger = logging.getLogger(__name__)

locations_blueprint = Blueprint('locations_routers', __name__, url_prefix='/api/locations_routers/')


@locations_blueprint.route('/get', methods=('GET',))
def get_all_locations():
    response: ResponseTemplate = ResponseTemplate()
    with open(JSON_LOCATIONS_PATH, "r") as json_file:
        response.__dict__.update(load(json_file))
    response.success = True
    return jsonify(response.__dict__)


@locations_blueprint.route('/update', methods=("POST", "OPTIONS"))
def update_list_locations_routers():
    if request.method == "OPTIONS":
        return jsonify(message="")

    response: ResponseTemplate = ResponseTemplate()
    data_json: dict = request.get_json(silent=True)

    try:
        router_group_name: str = data_json["routerGroupName"]
        zabbix_routers: ZabbixRoutersInventory = ZabbixRoutersInventory(ZABBIX_SERVER_URL)
        locations_routers: Dict[str, str] = zabbix_routers.get(router_group_name)
        with open(JSON_LOCATIONS_PATH, "w") as json_file:
            dump(locations_routers, json_file)

        response.success = True

    except (ConnectionError, KeyError) as exc:
        response.error = ERROR_RESPONSE_MESSAGES[exc.__class__]
        logger.info(f"[-] List of locations routers isn't updated.")

    return jsonify(response.__dict__)
