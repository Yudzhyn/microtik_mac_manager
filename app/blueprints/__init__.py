# exceptions
from modules.zabbix_routers import ZabbixRouters
from modules.mikrotik_access_list import MikrotikAccessList
from ..database.exceptions import *

# - Constants -----------------------------------------------------------------

ERROR_RESPONSE_MESSAGES: dict = {
    # db
    ObjectAlreadyExists: "Об'єкт уже існує в базі даних.",
    AddObjectError: "Внутрішня помилка сервера.",
    ObjectNotFound: "Не вдалось знайти об'єкт в базі даних.",

    # zabbix
    ZabbixRouters.ZabbixHostGroupNotFound: "Група хостів з даним іменем в Zabbix не існує.",

    # mikrotik
    MikrotikAccessList.ConnectionFailed: "Проблема з підключенням до роутера.",
    MikrotikAccessList.MacNotValid: "МАС адрес не є валідним.",
    MikrotikAccessList.MacNotExists: "Даний МАС адрес відсутній списку роутера.",

    # other
    ConnectionError: "Помилка при під'єднанні на сервер. Проблема з мережею.",
    KeyError: "Ключ є не правильний або не існує в запиті."
}

# - Blueprints ----------------------------------------------------------------

from .host_group import host_group_bp
from .mikrotik_access_list import access_list_bp
