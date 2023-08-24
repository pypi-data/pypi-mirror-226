import logging

from ponder.core.sql_connection import SQLConnection
from ponder.engines.mssql.mssql_dialect import MSSQLDialect

ponder_logger = logging.getLogger(__name__)
client_logger = logging.getLogger("client logger")


class MSSQLConnection(SQLConnection):
    def __init__(self, connection, dialect=None):
        my_dialect = MSSQLDialect() if dialect is None else dialect
        super().__init__(connection, my_dialect)

    # Initialization which can be overrided by subclasses
    def initialize(self, connection, dialect):
        pass
