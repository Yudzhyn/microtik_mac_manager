# mikrotik
from routeros_api import RouterOsApiPool

# for validation MAC address
from re import compile, VERBOSE, IGNORECASE

# enum
from enum import Enum, auto as enum_auto

# constants and exceptions
from routeros_api.exceptions import *

# type hint
from typing import Optional, Dict, List
from routeros_api.resource import RouterOsResource
from re import Pattern

# for logging
from logging import getLogger

logger = getLogger(__name__)


class MikrotikAccessList:
    # --------------------------- Class vars ----------------------------------

    __slots__ = ["__ip", "__port", "__username", "__password", "__interface",
                 "__connection", "__access_list"]

    class Interface(Enum):
        WIFI = enum_auto()
        CAPSMAN = enum_auto()

    INTERFACE_COMMAND: Dict[Interface, str] = {
        Interface.WIFI: '/interface/wireless/access-list/',
        Interface.CAPSMAN: '/caps-man/access-list/',
    }

    __MAC_VALIDATOR: Pattern = compile(r"""
                                         (
                                             ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                                            |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                                         )
                                         """, VERBOSE | IGNORECASE)

    # --------------------------- Exceptions ----------------------------------

    # - Connection --------------------

    class ConnectionFailed(Exception):
        pass

    # - MAC ---------------------------

    class MacNotExists(Exception):
        pass

    class MacAlreadyExists(Exception):
        pass

    class MacNotValid(Exception):
        pass

    # --------------------------- Builder ------------------------------------

    def __init__(self, ip_address: str,
                 username: str, password: str,
                 port: int,
                 interface: Interface = Interface.CAPSMAN):
        self.__ip: str = ip_address
        self.__port: int = port
        self.__username: str = username
        self.__password: str = password
        self.__interface: MikrotikAccessList.Interface = interface
        self.__connection: Optional[RouterOsApiPool] = None
        self.__access_list: Optional[RouterOsResource] = None
        self.__connect_mikrotik()

    # --------------------------- Private methods -----------------------------

    def __connect_mikrotik(self) -> None:
        try:
            self.__connection: Optional[RouterOsApiPool] = RouterOsApiPool(
                self.__ip,
                username=self.__username,
                password=self.__password,
                port=self.__port,
                plaintext_login=True
            )

            self.__access_list = self.__connection.get_api().get_resource(self.INTERFACE_COMMAND[self.__interface])
            logger.info(f"[+] Connection is created to '{self.__ip}:{self.__port}'.")
            return

        except RouterOsApiConnectionError:
            logger.warning(f"[-] Connection failed to '{self.__ip}:{self.__port}'. ERROR: incorrect IP or PORT.")

        except RouterOsApiCommunicationError:
            logger.warning(f"[-] Connection failed to '{self.__ip}:{self.__port}'. ERROR: incorrect credentials.")

        raise MikrotikAccessList.ConnectionFailed

    def __del__(self):
        if self.__connection:
            self.__connection.disconnect()
            logger.debug(f"[+] Connection is closed with '{self.__ip}:{self.__port}'.")
    # --------------------------- Public methods ------------------------------

    def get(self) -> List[Dict[str, str]]:
        access_list: List[Dict[str, str]] = self.__access_list.get()
        if self.__interface == MikrotikAccessList.Interface.CAPSMAN:
            access_list = access_list[:-2]
        logger.info(f"[+] Got access list from '{self.__ip}:{self.__port}'.")
        return access_list

    def add_mac(self, mac: str, comment: str = "") -> None:

        if not self.__connection:
            raise MikrotikAccessList.ConnectionFailed

        self.__access_list.add(mac_address=mac, comment=comment, place_before='0')
        logger.info(f"[+] The MAC '{mac}' is added to '{self.__ip}:{self.__port}'.")

    def remove_mac(self, id_mac: str) -> None:
        mac_address: List[Dict[str, str]] = self.__access_list.get(id=id_mac)
        if not mac_address:
            logger.info(f"[-] The MAC with id '{id_mac}' doesn't exist in '{self.__ip}:{self.__port}'.")
            raise MikrotikAccessList.MacNotExists

        self.__access_list.remove(id=id_mac)
        logger.info(f"[+] The MAC '{mac_address[0]}' is removed from '{self.__ip}:{self.__port}'.")

    @staticmethod
    def is_mac_valid(mac: str) -> bool:
        return True if MikrotikAccessList.__MAC_VALIDATOR.match(mac) is not None else False
