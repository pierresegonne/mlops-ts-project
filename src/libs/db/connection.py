import logging
from typing import Any, Callable, Iterable, List, Mapping, Optional, cast

import psycopg2
from google.cloud import secretmanager

logger = logging.getLogger(__name__)


def get_gcp_secret(project_id: str, secret_id: str, version_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version
    name = client.secret_version_path(project_id, secret_id, version_id)

    # Access the secret version
    request = secretmanager.AccessSecretVersionRequest(
        name=name,
    )
    response = client.access_secret_version(request=request)

    # Return the secret payload
    payload = response.payload.data.decode("UTF-8")

    return payload


EMAP_PROJECT_ID = "tmrow-152415"
DB_HOST = "127.0.0.1"
DB_USER = "readonly"
DB_PASSWORD = get_gcp_secret(EMAP_PROJECT_ID, "READONLY_POSTGRES_PASSWORD", "latest")
DB_NAME = "electricitymap"
DB_PORT = "5432"


class Cursor(Iterable):
    def __enter__(self) -> "Cursor":
        pass

    def __exit__(self, exc, value, tb) -> None:
        pass

    def close(self) -> None:
        pass

    def execute(self, sql: str, parameters: Optional[Any] = None) -> None:
        pass

    def fetchone(self) -> Optional[Any]:
        pass

    def fetchmany(self, size: int) -> List[Any]:
        pass

    def fetchall(self) -> List[Any]:
        pass


class Connection:

    dsn: str

    cursor: Callable[..., Cursor]

    closed: bool

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def close(self) -> None:
        pass


_pg_connection: Optional[Connection] = None


def set_pg_connection(server_config: Mapping[str, str]):
    global _pg_connection
    connection: Connection = psycopg2.connect(**server_config)
    _pg_connection = connection


def get_pg_connection(force_reconnect=False) -> Connection:
    """
    Get a database connection.

    Note that the connection is a singleton, so do not store the connection so
    it shouldn't be cached call-site. If the database connection is closed, we do
    return a new connection.

    In case the database connection is in a bad state (e.g. when a transaction is aborted),
    the force_reconnect parameter can be used.
    """
    global _pg_connection
    if _pg_connection and not _pg_connection.closed:
        # We already have a connection that isn't closed
        if force_reconnect:
            # NOTE: force reconnect is needed in the case where the connection is in
            # a bad state (e.g. when a transaction is aborted)
            logger.info("Database connection: force reconnecting")
            _pg_connection = cast(Connection, psycopg2.connect(dsn=_pg_connection.dsn))
            return _pg_connection
        return _pg_connection

    if not _pg_connection:
        logger.info("Database connection: connecting")

    if _pg_connection and _pg_connection.closed:
        logger.info("Database connection: reconnecting as connection was closed")

    connection: Connection = psycopg2.connect(
        user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME
    )
    _pg_connection = connection

    return connection
