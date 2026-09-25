import os
import oracledb

ORACLE_CLIENT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "oracle",
    "instantclient_21_23"
)

oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)


def get_connection():
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]
    dsn = os.environ["DB_DSN"]
    return oracledb.connect(user=user, password=password, dsn=dsn)