import json
from pathlib import Path
from sqlalchemy import create_engine


def get_engines(config_file=None):
    """
    Gets a dict of engine configured in the file

    Parameters
    -------------
    config_file: str
        The json file with engine connections
        If None searches for '.dbconnections.json' in user directory

    Returns
    -------------
    dict of sqlalchemy.engine.Engine


    .. note:: Support for SQL-Server (pymssql) and PostgreSQL (psycopg2)

    """

    dbman = DBConnectionManager(config_file=config_file)
    return {conn_name: dbman.get_engine(conn_name) for conn_name, _ in dbman.connections}


class DBConnectionManager:
    """
    Reads a json file with connection configurations and keeps a list of connection available that file

    Each object in the file must have the attributes ("type", "user", "pwd", "host", "database"):

            - "type" is the type of database (SQL Server, PostgreSQL, etc...):
                'sql-server' or 'mssql' for SQL Server

                'postgres' or 'postgresql' for PostgreSQL
            - "user" an user in the database server
            - "pwd" user password
            - "host" hostname
            - "database" database of connection

    .. note:: Support for SQL-Server (pymssql) and PostgreSQL (psycopg2)
    """

    def __init__(self, config_file=''):
        """

        Constructor

        Loads a json file with connection parameters and setup the engines

        Parameters
        ----------
        config_file: str
            Filename of connection configuration file. If '', try to load a file in user folder named .dbconnections.json



        Raises
        ----------
        Exception
            If read of file fails
        """

        if not config_file:
            config_file = str(Path.home()) + '/.dbconnections.json'

        with open(config_file) as file:
            self.__configs = json.load(file)

    @property
    def connections(self):
        """
        Returns name and type of connections

        Returns
        -------
        list of tuple of (str, str)
            Each tuple corresponding of (name, type)
        """
        return [(key, self.__configs[key]['type']) for key in self.__configs]

    def get_engine(self, connection_name, **kwargs):
        """
        Returns a sqlalchemy engine with the **connection_name** connection bind to it

        Parameters
        ----------
        connection_name: str
            Name of a connection object in **config_file**


        Returns
        -------
        sqlalchemy.engine.Engine
        """

        conn_dict = self.__configs[connection_name]

        if conn_dict['type'] in ('sql-server', 'mssql'):
            conn_str = self.__get_mssql_connection_string(conn_dict)
        elif conn_dict['type'] in ('postgres', 'postgresql'):
            conn_str = self.__get_postgres_connection_string(conn_dict)
        else:
            raise ValueError('banco ' + conn_dict['type'] + 'não suportado')

        return create_engine(conn_str, **kwargs)

    def __get_mssql_connection_string(self, conn_dict):
        conn_str = 'mssql+pymssql://' + conn_dict['user'] + ':' + conn_dict['pwd'] + '@' + conn_dict['host'] + '/' + \
                   conn_dict['database']
        return conn_str

    def __get_postgres_connection_string(self, conn_dict):
        conn_str = "postgresql+psycopg2://" + conn_dict['user'] + ':' + conn_dict['pwd'] + '@' + \
                   conn_dict['host'] + '/' + conn_dict['database']
        return conn_str

