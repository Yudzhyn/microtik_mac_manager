# sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# exceptions
from sqlalchemy.exc import IntegrityError
from .exceptions import ObjectAlreadyExists, AddObjectError, ObjectNotFound, DeleteObjectError

# type hints
from typing import List, Optional

# for logging
import logging

logger = logging.getLogger(__name__)

db: SQLAlchemy = SQLAlchemy()


# - Useful functions ----------------------------------------------------------

def db_add(sql_object: db.Model) -> None:
    try:
        db.session.add(sql_object)
        db.session.commit()
        logger.info(f"[+] {sql_object} created.")

    except IntegrityError:
        raise ObjectAlreadyExists(sql_object)

    except Exception as exc:
        raise AddObjectError(sql_object, exc)


def db_delete(sql_object: db.Model) -> None:
    try:
        db.session.delete(sql_object)
        db.session.commit()
        logger.info(f"[+] {sql_object} deleted.")

    except Exception as exc:
        raise DeleteObjectError(sql_object, exc)


def db_get_all(sql_model: db.Model) -> List[db.Model]:
    return sql_model.query.all()


def db_get_by_id(sql_model: db.Model, _id: int) -> db.Model:
    sql_object: Optional[HostGroup] = sql_model.query.filter(sql_model.id == _id).first()
    if not sql_object:
        raise ObjectNotFound(sql_model, _id)

    return sql_object


# - Models --------------------------------------------------------------------

from .host_group import HostGroup
from .host_router import HostRouter
