import time
from core.oracle_pool import get_db_connection

def check_oracle_health() -> dict:
    """Executa checagem de conectividade: SYSDATE e os 10 primeiros owners."""
    start_time = time.perf_counter()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # 1. Sysdate e contexto da sessão
            cur.execute("SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD\"T\"HH24:MI:SS') AS DB_SYSDATE, SYS_CONTEXT('USERENV', 'SESSION_USER') AS CURRENT_USER FROM DUAL")
            row = cur.fetchone()
            db_sysdate = row[0] if row else None
            session_user = row[1] if row else None

            # 2. Amostra de 10 owners
            cur.execute("SELECT USERNAME FROM ALL_USERS WHERE ROWNUM <= 10 ORDER BY USERNAME")
            owners = [r[0] for r in cur.fetchall()]

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    return {
        "status": "ONLINE",
        "service": "OracleInternalApi",
        "mode": "Oracle Thick Mode (Instant Client 21.23)",
        "latencyMs": elapsed_ms,
        "database": {
            "sysdate": db_sysdate,
            "sessionUser": session_user,
            "totalSampleOwners": len(owners),
            "sampleOwners": owners,
        },
    }
