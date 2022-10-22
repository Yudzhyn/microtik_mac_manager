# sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# exceptions
from sqlalchemy.exc import IntegrityError
from .exceptions import ObjectAlreadyExists, AddToDBError, ObjectNotFound

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
        raise AddToDBError(sql_object, exc)


def db_get_all(sql_model: db.Model) -> List[db.Model]:
    return db.session.query(sql_model).all()


def db_get_by_id(sql_model: db.Model, _id: int) -> db.Model:
    sql_object: Optional[HostGroup] = db.session.query(sql_model).filter(sql_model.id == _id).first()
    if not sql_object:
        raise ObjectNotFound(sql_model, _id)

    return sql_object


# - Models --------------------------------------------------------------------

from .host_group import HostGroup
