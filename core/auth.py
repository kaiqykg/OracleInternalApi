from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from core.config import API_KEY

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Valida o cabeçalho x-api-key da requisição."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho 'x-api-key' ausente.",
        )
    if api_key.strip() != API_KEY.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida.",
        )
    return api_key
