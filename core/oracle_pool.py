import oracledb
from contextlib import contextmanager
from typing import Generator
from core.config import (
    ORACLE_CLIENT_PATH,
    DB_USER,
    DB_PASS,
    DB_DSN,
    validate_config,
)

_client_initialized = False
_pool: oracledb.ConnectionPool | None = None

def init_thick_client() -> None:
    """Inicializa o Oracle Client em Thick Mode uma única vez."""
    global _client_initialized
    if not _client_initialized:
        validate_config()
        try:
            oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
        except oracledb.ProgrammingError as e:
            # Já inicializado anteriormente no mesmo processo
            if "already been initialized" not in str(e):
                raise
        _client_initialized = True

def init_pool(min_conn: int = 2, max_conn: int = 10, increment: int = 1) -> oracledb.ConnectionPool:
    """Cria e inicializa o pool de conexões persistente."""
    global _pool
    init_thick_client()
    if _pool is None:
        _pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN,
            min=min_conn,
            max=max_conn,
            increment=increment,
            getmode=oracledb.POOL_GETMODE_WAIT,
        )
    return _pool

def close_pool() -> None:
    """Encerra o pool de conexões com segurança."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None

@contextmanager
def get_db_connection() -> Generator[oracledb.Connection, None, None]:
    """Context manager para adquirir e devolver uma conexão ao pool."""
    global _pool
    if _pool is None:
        init_pool()
    conn = _pool.acquire()
    try:
        yield conn
    finally:
        _pool.release(conn)
