import sqlalchemy


def get_engine(configuration: dict) -> sqlalchemy.Connection:
    """
    Returns a connection to the database specified in the configuration.
    This connection can be passed around to other functions that need to interact with the database.
    """
    return sqlalchemy.engine_from_config(configuration)
