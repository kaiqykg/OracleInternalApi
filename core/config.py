import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório raiz da API interna
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Carrega variáveis da API (PORT, HOST, API_KEY)
app_env_path = BASE_DIR / ".env"
if app_env_path.exists():
    load_dotenv(dotenv_path=app_env_path)

# 2. Carrega variáveis de conexão do Oracle (DB_USER, DB_PASS, DB_DSN)
db_env_path = BASE_DIR / "oracleDb secret" / ".env"
if db_env_path.exists():
    load_dotenv(dotenv_path=db_env_path, override=True)

# 3. Caminho do Oracle Instant Client (Thick Mode)
ORACLE_CLIENT_PATH = str(BASE_DIR / "oracle" / "instantclient_21_23")

# Configurações do Serviço
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "3005"))
API_KEY: str = os.getenv("API_KEY", "pcm_oracle_internal_key_2026")

# Credenciais Oracle
DB_USER: str = os.getenv("DB_USER", "")
DB_PASS: str = os.getenv("DB_PASS", "")
DB_DSN: str = os.getenv("DB_DSN", "")

def validate_config() -> None:
    """Valida se os requisitos mínimos de runtime estão atendidos."""
    if not os.path.isdir(ORACLE_CLIENT_PATH):
        raise RuntimeError(
            f"Diretório do Oracle Instant Client não encontrado em: {ORACLE_CLIENT_PATH}"
        )
    if not DB_USER or not DB_PASS or not DB_DSN:
        raise RuntimeError(
            "Credenciais do banco Oracle (DB_USER, DB_PASS, DB_DSN) não foram localizadas em 'oracleDb secret/.env'"
        )
