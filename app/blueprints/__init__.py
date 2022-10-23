# exceptions
from requests.exceptions import ConnectionError
from modules.zabbix_routers import ZabbixRouters
from ..database.exceptions import *

# - Constants -----------------------------------------------------------------

ERROR_RESPONSE_MESSAGES: dict = {
    ObjectAlreadyExists: "Об'єкт уже існує в базі даних.",
    AddObjectError: "Внутрішня помилка сервера.",
    ObjectNotFound: "Не вдалось знайти об'єкт в базі даних.",
    ZabbixRouters.ZabbixHostGroupNotFound: "Група хостів з даним іменем в Zabbix не існує.",
    ConnectionError: "Помилка при під'єднанні на сервер. Проблема з мережею.",
    KeyError: "Ключ є не правильний або не існує в запиті."
}

# - Blueprints ----------------------------------------------------------------

from .host_group import host_group_bp
