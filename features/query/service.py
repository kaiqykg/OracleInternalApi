import time
import datetime
import decimal
import re
import oracledb
from typing import Any
from core.oracle_pool import get_db_connection

def serialize_oracle_val(val: Any) -> Any:
    """Converte tipos nativos do Oracle/Python para tipos serializáveis em JSON."""
    if val is None:
        return None
    if isinstance(val, (datetime.datetime, datetime.date)):
        return val.isoformat()
    if isinstance(val, decimal.Decimal):
        return float(val) if val % 1 else int(val)
    if isinstance(val, oracledb.LOB):
        return val.read()
    if isinstance(val, bytes):
        try:
            return val.decode("utf-8")
        except UnicodeDecodeError:
            return val.hex()
    return val

def execute_oracle_query(sql: str, params: Any, output_format: str) -> dict:
    """Executa a query SQL e retorna os dados no formato solicitado ('records' ou 'table')."""
    clean_sql = sql.strip().rstrip(";")
    
    # Se params for um dicionário, filtra para manter apenas as chaves presentes como ':bind_var'
    # no comando SQL, prevenindo o erro ORA-01036 (illegal variable name/number).
    if isinstance(params, dict):
        bind_names = set(re.findall(r":([a-zA-Z0-9_]+)", clean_sql))
        query_params = {k: v for k, v in params.items() if k in bind_names}
    else:
        query_params = params if params is not None else {}

    start_time = time.perf_counter()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(clean_sql, query_params)

            if not cur.description:
                # Comandos que não retornam dataset
                elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                return {
                    "success": True,
                    "format": output_format,
                    "totalRows": 0,
                    "executionTimeMs": elapsed_ms,
                    "columns": [],
                    "rows": [] if output_format == "table" else None,
                    "data": [] if output_format == "records" else None,
                }

            columns = [desc[0] for desc in cur.description]
            raw_rows = cur.fetchall()
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

            if output_format == "table":
                serialized_rows = [
                    [serialize_oracle_val(val) for val in row] for row in raw_rows
                ]
                return {
                    "success": True,
                    "format": "table",
                    "totalRows": len(serialized_rows),
                    "executionTimeMs": elapsed_ms,
                    "columns": columns,
                    "rows": serialized_rows,
                }

            # records format (default)
            records = [
                {col: serialize_oracle_val(val) for col, val in zip(columns, row)}
                for row in raw_rows
            ]
            return {
                "success": True,
                "format": "records",
                "totalRows": len(records),
                "executionTimeMs": elapsed_ms,
                "columns": columns,
                "data": records,
            }
