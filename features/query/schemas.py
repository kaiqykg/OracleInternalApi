from typing import Any, Literal
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    sql: str = Field(..., description="Instrução SQL a ser executada no Oracle")
    params: dict[str, Any] | list[Any] | None = Field(
        default=None, description="Parâmetros opcionais para a query (bind variables)"
    )
    format: Literal["records", "table"] = Field(
        default="records",
        description="Formato de retorno: 'records' (lista de objetos) ou 'table' (matriz compacta)",
    )

class QueryResponse(BaseModel):
    success: bool
    format: str
    totalRows: int
    executionTimeMs: float
    columns: list[str] | None = None
    rows: list[list[Any]] | None = None
    data: list[dict[str, Any]] | None = None
    error: str | None = None
