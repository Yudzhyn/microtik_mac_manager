# for logging
import logging

logger = logging.getLogger(__name__)


# - DataBase ------------------------------------------------------------------

class AddObjectError(Exception):
    def __init__(self, sql_object, exc):
        logger.error(f"[-] Error during adding {sql_object} to database. Error: {exc}")


class DeleteObjectError(Exception):
    def __init__(self, sql_object, exc):
        logger.error(f"[-] Error during deleting {sql_object} from database. Error: {exc}")


class ObjectAlreadyExists(Exception):
    def __init__(self, sql_object):
        logger.error(f"[-] Error while adding {sql_object} to database. Object already exists.")


class ObjectNotFound(Exception):
    def __init__(self, sql_object, _id: int):
        logger.info(f"[-] {sql_object} with id '{_id}' not found.")
# - HostGroup ------------------------------------------------------------------
