import psycopg
from core.config import settings


async def get_db_connection():
    """Return an async psycopg connection using psycopg v3 API.

    Note: the module `psycopg.async_` does not exist. The async connection
    class is available on the top-level `psycopg` package as
    `psycopg.AsyncConnection` when `psycopg` (v3) is installed.
    """
    dsn = (
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password} "
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port}"
    )
    conn = await psycopg.AsyncConnection.connect(dsn)
    return conn
