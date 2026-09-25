from fastapi import APIRouter, HTTPException, status
from features.health.service import check_oracle_health

router = APIRouter()

@router.get("/status", summary="Checagem de Saúde do Oracle")
async def health_status():
    """Retorna o status operacional, SYSDATE do banco e primeiros 10 owners."""
    try:
        return check_oracle_health()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Falha de comunicação com o banco Oracle: {str(e)}",
        )
