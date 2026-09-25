from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import verify_api_key
from features.query.schemas import QueryRequest, QueryResponse
from features.query.service import execute_oracle_query

router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.post("/query", response_model=QueryResponse, summary="Executa Consulta SQL")
async def run_query(payload: QueryRequest):
    """Executa SQL no Oracle via conexão nativa Thick Mode persistente."""
    try:
        result = execute_oracle_query(
            sql=payload.sql,
            params=payload.params,
            output_format=payload.format,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro na execução da query: {str(e)}",
        )
