from sqlalchemy import inspect

from heinlein.io.db.db import get_engine

config = {
    "sqlalchemy.url": "sqlite:////Volumes/workspace/data/des/catalogs/tiled/sql/des.db"
}
engine = get_engine(config)
inspector = inspect(engine)
print(inspector.get_table_names())
