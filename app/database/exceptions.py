# for logging
import logging

logger = logging.getLogger(__name__)


# - DataBase ------------------------------------------------------------------

class AddToDBError(Exception):
    def __init__(self, sql_object, exc):
        logger.error(f"[-] Error while adding {sql_object} to database. Unknown error: {exc}")


class ObjectAlreadyExistsInDB(Exception):
    def __init__(self, sql_object):
        logger.error(f"[-] Error while adding {sql_object} to database. Object already exists.")
