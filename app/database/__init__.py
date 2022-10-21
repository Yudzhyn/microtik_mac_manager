# sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# exceptions
from sqlalchemy.exc import IntegrityError
from .exceptions import ObjectAlreadyExistsInDB, AddToDBError

# for logging
import logging

logger = logging.getLogger(__name__)

db: SQLAlchemy = SQLAlchemy()


# - Useful functions ----------------------------------------------------------

def db_add(sql_object: db.Model) -> None:
    try:
        db.session.add(sql_object)
        db.session.commit()

    except IntegrityError:
        raise ObjectAlreadyExistsInDB(sql_object)

    except Exception as exc:
        raise AddToDBError(sql_object, exc)


# - Models --------------------------------------------------------------------

