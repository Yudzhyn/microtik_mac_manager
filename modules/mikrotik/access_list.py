# mikrotik
from routeros_api import RouterOsApiPool

# for validation MAC address
from re import compile, VERBOSE, IGNORECASE

# enum
from enum import Enum, auto as enum_auto

# constants and exceptions
from routeros_api.exceptions import *

# type hint
from typing import Optional, Dict, List, Callable
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

    class ConnectionNotCreated(Exception):
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

        raise ConnectionError

    def __del__(self):
        if self.__connection:
            self.__connection.disconnect()
            logger.debug(f"[+] Connection is closed with '{self.__ip}:{self.__port}'.")

    # DECORATOR
    def __check_connection(func: Callable) -> Callable:
        def __decorator(self):
            if not self.__connection:
                logger.warning(f"[-] Connection is not created for '{self.__ip}:{self.__port}'.")
                raise MikrotikAccessList.ConnectionNotCreated
            return func(self)

        return __decorator

    # --------------------------- Public methods ------------------------------

    @__check_connection
    def get(self) -> List[Dict[str, str]]:
        access_list: List[Dict[str, str]] = self.__access_list.get()
        logger.info(f"[+] Got access list from '{self.__ip}:{self.__port}'.")
        return access_list

    @__check_connection
    def add_mac(self, mac: str, comment: str = "", validate_mac: bool = False) -> None:

        if not self.__connection:
            raise MikrotikAccessList.ConnectionNotCreated

        if validate_mac and MikrotikAccessList.is_mac_valid(mac):
            logger.warning(f"[+] The MAC '{mac}' is not valid.")
            raise MikrotikAccessList.MacNotValid

        self.__access_list.add(mac_address=mac, comment=comment, place_before='0')
        logger.info(f"[+] The MAC '{mac}' is added to '{self.__ip}:{self.__port}'.")

    @__check_connection
    def remove_mac(self, mac: str) -> None:
        access_list_table: List[Dict] = self.get()
        access_list_item: Dict = next((item for item in access_list_table if item.get("mac-address") == mac), None)

        if not access_list_item:
            logger.warning(f"[+] The MAC '{mac}' doesn't exist in '{self.__ip}:{self.__port}'.")
            raise MikrotikAccessList.MacNotExists

        self.__access_list.remove(id=access_list_item["id"])
        logger.info(f"[+] The MAC '{mac}' is removed from '{self.__ip}:{self.__port}'.")

    @staticmethod
    def is_mac_valid(mac: str) -> bool:
        return True if MikrotikAccessList.__MAC_VALIDATOR.match(mac) is not None else False
