# zabbix
from pyzabbix import ZabbixAPI
from os import environ

# type hints
from typing import Optional, List, Dict

# for logging
from logging import getLogger

logger = getLogger(__name__)


class ZabbixRouters:

    # --------------------------- Builder -------------------------------------
    def __init__(self, url_server: str):
        # private
        self.__url_server: str = url_server
        self.__login: str = environ["ZABBIX_LOGIN"]
        self.__password: str = environ["ZABBIX_PASS"]

        self.__zapi: Optional[ZabbixAPI] = None
        self.__connect_zabbix()

    # --------------------------- Exceptions ----------------------------------

    class ZabbixHostGroupNotFound(Exception):
        def __init__(self, name: str):
            logger.info(f"[-] Host group '{name}' not found.")

    # --------------------------- Private methods -----------------------------
    def __connect_zabbix(self):
        self.__zapi = ZabbixAPI(self.__url_server)
        self.__zapi.login(self.__login, self.__password)

    # --------------------------- Public methods ------------------------------
    def get_host_group_routers(self, name: str):
        host_group: List[Dict[str, str]] = self.__zapi.hostgroup.get(filter={"name": name})
        if not host_group:
            raise ZabbixRouters.ZabbixHostGroupNotFound(name)

        hosts_describes: List[Dict[str, str]] = self.__zapi.host.get(groupids=host_group[0]["groupid"])
        hosts_interfaces: List[Dict[str, str]] = self.__zapi.hostinterface.get(groupids=host_group[0]["groupid"])

        hosts_parsed: List[Dict[str, str]] = []
        for host in hosts_describes:
            host_id = host["hostid"]
            host_interface: Optional[dict] = \
                next((host_infc for host_infc in hosts_interfaces if host_infc["hostid"] == host_id), None)
            if not host_interface:
                continue
            hosts_parsed.append({"name": host["name"], "ip": host_interface["ip"], "id": int(host_interface["hostid"])})
        return hosts_parsed

    def get_host_group_id(self, name: str) -> int:
        host_group: List[Dict[str, str]] = self.__zapi.hostgroup.get(filter={"name": name})
        if not host_group:
            raise ZabbixRouters.ZabbixHostGroupNotFound(name)
        return int(host_group[0]["groupid"])
