# flask
from flask import request, jsonify, Blueprint

# db
from ..database import HostGroup, HostRouter, db_get_all, db_add, db_delete, db_get_by_id
from ..database.exceptions import *

# location list
from modules import ZabbixRouters
from requests.exceptions import ConnectionError
from configs import ZABBIX_SERVER_URL

# response
from . import ERROR_RESPONSE_MESSAGES

# for logging
import logging

logger = logging.getLogger(__name__)

host_group_bp = Blueprint('host_group', __name__, url_prefix='/api/host_group/')


@host_group_bp.route('', methods=("GET",))
def get_all_host_groups():
    return jsonify(
        {
            "error": None,
            "elements": [{"id": group.id, "name": group.name} for group in db_get_all(HostGroup)]
        }
    )


@host_group_bp.route('/routers', methods=("GET",))
def get_host_group_routers():
    try:
        host_group_id: str = request.args["id"]
        host_group: HostGroup = db_get_by_id(HostGroup, host_group_id)
        return jsonify(
            {
                "error": None,
                "elements": [{"id": router.id, "name": router.name} for router in host_group.host_routers]

            }
        )

    except ObjectNotFound as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})


@host_group_bp.route('', methods=("PUT",))
def add_host_group():
    try:
        host_group_name: str = request.args["name"]
        zabbix: ZabbixRouters = ZabbixRouters(ZABBIX_SERVER_URL)
        host_group_zabbix_id: int = zabbix.get_host_group_id(host_group_name)
        db_add(HostGroup(id=host_group_zabbix_id, name=host_group_name))
        return jsonify({"error": None})

    except (ZabbixRouters.ZabbixHostGroupNotFound, ConnectionError, AddObjectError, ObjectAlreadyExists) as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})


@host_group_bp.route('', methods=("DELETE",))
def delete_host_group():
    try:
        host_group_id: int = request.args.get("id", type=int)
        host_group: HostGroup = db_get_by_id(HostGroup, host_group_id)
        for router in host_group.host_routers:
            db_delete(router)
        db_delete(host_group)
        return jsonify({"error": None})

    except ObjectNotFound as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})


@host_group_bp.route('', methods=("POST",))
def update_host_group_routers():
    try:
        host_group_id: int = request.args.get("id", type=int)
        host_group: HostGroup = db_get_by_id(HostGroup, host_group_id)
        for router in host_group.host_routers:
            db_delete(router)
        zabbix: ZabbixRouters = ZabbixRouters(ZABBIX_SERVER_URL)
        host_group_routers: list = zabbix.get_host_group_routers(host_group.name)
        for router in host_group_routers:
            db_add(HostRouter(id=router["id"], name=router["name"], ip=router["ip"], host_group=host_group))

        return jsonify({"error": None})

    except ObjectNotFound as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})
