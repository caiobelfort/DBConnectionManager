import json
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import engine


def _get_connection_driver(dialect: str) -> str:
    """
    Returns the driver for the database
    Args:
        dialect: Type of database

    Returns:
        The driver for engine creation
    """

    if dialect == 'mssql':
        return 'pymssql'
    elif dialect == 'postgres':
        return 'psycopg2'
    else:
        raise ValueError('database vendor %s not supported' % dialect)


def get_engine(connection_name: str,
               config_file: str or None = None,
               **kwargs
               ) -> engine.Engine:
    """
    Returns an engine from a configuration file
    Args:
        connection_name: Name of connection
        config_file: Configuration file where the *connection_name* parameters are declared. Only JSON
    Returns:
        A SQLAlchemy engine
    """

    # Loads the json data as dict
    filename = config_file if config_file is not None else str(Path.home()) + '/.dbconnections.json'

    with open(filename, 'r') as file:
        connections = json.load(file)

    # Check if connection name exists in configuration file
    if connection_name not in connections:
        raise ValueError("%s connection don't exists in %s" % (connection_name, filename))

    conf = connections[connection_name]

    # Check if connection configuration have all required variables
    _check_required_attrs(conf, connection_name)

    # Get connection configurations
    dialect = conf['type']
    driver = _get_connection_driver(dialect)
    hostname = conf['host'] + ':' + conf['port'] if 'port' in conf else conf['host']
    user = conf['user']
    pwd = conf['pwd']
    database = conf['database']

    # Connection string
    cstr = '{}+{}://{}:{}@{}/{}'.format(dialect, driver, user, pwd, hostname, database)

    return sa.create_engine(cstr, **kwargs)


def _check_required_attrs(connection_conf, connection_name):
    error_string = 'Required Attribute %s not declared in configuration file for connection %s.'
    required_attr = ('type', 'user', 'pwd', 'host', 'database')
    for v in required_attr:
        if v not in connection_conf:
            raise ValueError(error_string % (v, connection_name))

