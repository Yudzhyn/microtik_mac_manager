# for logging
import logging

logger = logging.getLogger(__name__)


# - DataBase ------------------------------------------------------------------

class AddToDBError(Exception):
    def __init__(self, sql_object, exc):
        logger.error(f"[-] Error while adding {sql_object} to database. Unknown error: {exc}")


class ObjectAlreadyExists(Exception):
    def __init__(self, sql_object):
        logger.error(f"[-] Error while adding {sql_object} to database. Object already exists.")


class ObjectNotFound(Exception):
    def __init__(self, sql_object, _id: int):
        logger.info(f"[-] {sql_object.__class__} with id '{_id}' not found.")
# - HostGroup ------------------------------------------------------------------
