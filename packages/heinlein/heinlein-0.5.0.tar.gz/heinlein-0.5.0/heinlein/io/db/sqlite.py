from pathlib import Path

import sqlalchemy

from heinlein.io.db.exceptions import heinleinDatabaseException


def get_sqlite_engine(configuration: dict) -> sqlalchemy.Engine:
    if not (path := configuration.get("path")):
        raise heinleinDatabaseException("No path specified in configuration.")
    elif not (path := Path(path)).exists() or not path.is_file():
        raise heinleinDatabaseException(
            f"Path {path} does not exist or is not a sqlite database."
        )
    return sqlalchemy.create_engine(f"sqlite:///{path}")
