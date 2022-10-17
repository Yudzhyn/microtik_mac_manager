# zabbix
from pyzabbix import ZabbixAPI
from os import environ

# type hints
from typing import Optional, List, Dict

# for logging
from logging import getLogger

logger = getLogger(__name__)


class ZabbixRoutersInventory:

    # --------------------------- Builder ------------------------------------
    def __init__(self, url_server: str):
        # private
        self.__url_server: str = url_server
        self.__login: str = environ["ZABBIX_LOGIN"]
        self.__password: str = environ["ZABBIX_PASS"]

        self.__zapi: Optional[ZabbixAPI] = None
        self.__connect_zabbix()

    # --------------------------- Private methods -----------------------------
    def __connect_zabbix(self):
        self.__zapi = ZabbixAPI(self.__url_server)
        self.__zapi.login(self.__login, self.__password)

    # --------------------------- Public methods ------------------------------
    def get(self, host_group_name: str):
        host_group: List[Dict[str, str]] = self.__zapi.hostgroup.get(
            filter={"name": host_group_name}
        )
        if not host_group:
            pass

        hosts_describes: List[Dict[str, str]] = self.__zapi.host.get(groupids=host_group[0]["groupid"])
        hosts_interfaces: List[Dict[str, str]] = self.__zapi.hostinterface.get(groupids=host_group[0]["groupid"])

        hosts_parsed: List[Dict[str, str]] = []
        for host in hosts_describes:
            host_id = host["hostid"]
            host_interface: Optional[dict] = \
                next((host_infc for host_infc in hosts_interfaces if host_infc["hostid"] == host_id), None)
            if not host_interface:
                continue
            hosts_parsed.append({"name": host["name"], "ip": host_interface["ip"], })
        return hosts_parsed
