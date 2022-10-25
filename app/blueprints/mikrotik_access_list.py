# flask
from flask import request, jsonify, Blueprint

# db
from ..database import HostRouter, db_get_by_id
from ..database.exceptions import ObjectNotFound

# mikrotik
from modules import MikrotikAccessList
from os import environ

# constants
from . import ERROR_RESPONSE_MESSAGES

access_list_bp: Blueprint = Blueprint('access_list', __name__, url_prefix='/api/access_list')

MIKROTIK_LOGIN: str = environ["MIKROTIK_LOGIN"]
MIKROTIK_PASS: str = environ["MIKROTIK_PASSWORD"]


@access_list_bp.route('', methods=("GET",))
def get_access_list():
    try:
        host_router_id: int = request.args.get("host_router_id", type=int)
        host_router: HostRouter = db_get_by_id(HostRouter, host_router_id)
        access_list: MikrotikAccessList = MikrotikAccessList(
            ip_address=host_router.ip,
            username=MIKROTIK_LOGIN,
            password=MIKROTIK_PASS,
            port=host_router.port
        )
        return jsonify(
            {
                "error": None,
                "access_list": access_list.get()
            }
        )
    except (MikrotikAccessList.ConnectionFailed, ObjectNotFound) as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})


@access_list_bp.route('', methods=("PUT",))
def add_mac():
    data_json: dict = request.get_json(silent=True)
    try:
        host_router_id: int = data_json["host_router_id"]
        mac_address: str = data_json["mac"]
        comment: str = data_json["comment"]

        if not MikrotikAccessList.is_mac_valid(mac_address):
            raise MikrotikAccessList.MacNotValid

        host_router: HostRouter = db_get_by_id(HostRouter, host_router_id)
        access_list: MikrotikAccessList = MikrotikAccessList(
            ip_address=host_router.ip,
            username=MIKROTIK_LOGIN,
            password=MIKROTIK_PASS,
            port=host_router.port
        )
        access_list.add_mac(mac_address, comment)
        return jsonify({"error": None})

    except (MikrotikAccessList.ConnectionFailed, MikrotikAccessList.MacNotValid,
            ObjectNotFound, KeyError) as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})


@access_list_bp.route('', methods=("DELETE",))
def delete_mac():
    data_json: dict = request.get_json(silent=True)
    try:
        host_router_id: int = data_json["host_router_id"]
        mac_id: str = data_json["mac_id"]

        host_router: HostRouter = db_get_by_id(HostRouter, host_router_id)
        access_list: MikrotikAccessList = MikrotikAccessList(
            ip_address=host_router.ip,
            username=MIKROTIK_LOGIN,
            password=MIKROTIK_PASS,
            port=host_router.port
        )
        access_list.remove_mac(mac_id)
        return jsonify({"error": None})

    except (MikrotikAccessList.ConnectionFailed, MikrotikAccessList.MacNotExists, ObjectNotFound, KeyError) as exc:
        return jsonify({"error": ERROR_RESPONSE_MESSAGES[exc.__class__]})
