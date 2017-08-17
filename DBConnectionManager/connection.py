import json
from pathlib import Path
from sqlalchemy import create_engine

"""
Módulo de conexão com banco

Todas as conexões são administradas por um arquivo de configuração
"""


class DatabaseConnectionManager:
    """
    Lê arquivo de configuração e administra conexões fornecidas no arquivo
    """

    def __init__(self, config_file=''):
        """
        Construtor de instância.

        Verifica arquivo de configuração e fornece nomes de conexões definidas no arquivo

        Parameters
        ----------
        config_file: str
            Nome do arquivo de configuração em formato json, se não for definido utiliza $HOME/.gmdb.json

            Cada objeto de conexão deve possuir os campos ("type", "user", "pwd", "host", "database")

            - "type" é utilizado para inferir o tipo do banco de dados (SQL Server, PostgreSQL, etc...)
            - "user" deve possuir um usuário cadastrado pelo administrador do banco
            - "pwd" deve conter a senha do usuário fornecido
            - "host" deve conter o endereço para o banco de dados
            - "database" deve conter o schema desejado a acessar

        Raises
        ----------
        Exception
            Se a leitura do arquivo falhar
        """

        if not config_file:
            config_file = str(Path.home()) + '/.gmdb.json'

        with open(config_file) as file:
            self.__configs = json.load(file)

    @property
    def connection_names(self):
        """
        Retorna nome das conexões configuradas

        Returns
        -------
        list of str
        """

        return [key for key in self.__configs]

    def get_connection(self, connection_name):
        """
        Cria conexão

        Parameters
        ----------
        connection_name: str
            Nome da conexão no arquivo de conexão

        Returns
        -------
        sqlalchemy.engine.Engine

        """

        conn_dict = self.__configs[connection_name]

        if conn_dict['type'] in ('sql-server', 'mssql'):
            return self.__get_mssql_connection(conn_dict)
        elif conn_dict['type'] in ('postgres', 'postgresql'):
            return self.__get_postgres_connection(conn_dict)
        else:
            raise ValueError('banco ' + conn_dict['type'] + 'não suportado')

    def __get_mssql_connection(self, conn_dict):
        conn_str = 'mssql+pymssql://' + conn_dict['user'] + ':' + conn_dict['pwd'] + '@' + conn_dict['host'] + '/' + \
                   conn_dict['database']
        return create_engine(conn_str)

    def __get_postgres_connection(self, conn_dict):
        conn_str = "postgresql+psycopg2://" + conn_dict['user'] + ':' + conn_dict['pwd'] + '@' + \
                   conn_dict['host'] + '/' + conn_dict['database']
        return create_engine(conn_str)
