from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import HOST, PORT
from core.oracle_pool import init_pool, close_pool
from features.health.router import router as health_router
from features.query.router import router as query_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização do Pool Oracle na subida do serviço
    init_pool()
    yield
    # Fechamento gracioso do Pool na descida
    close_pool()

app = FastAPI(
    title="Oracle Internal API (PCM)",
    version="1.0.0",
    description="Gateway interno de alta performance para o banco Oracle Corporativo (Thick Mode)",
    lifespan=lifespan,
)

# CORS liberado para comunicação interna de dashboards/microserviços
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das Fatias Verticais
app.include_router(health_router, prefix="/api", tags=["Health & Status"])
app.include_router(query_router, prefix="/api", tags=["SQL Query"])

@app.get("/", tags=["Root"])
def root():
    return {
        "service": "OracleInternalApi",
        "status": "ONLINE",
        "docsUrl": "/docs",
        "healthUrl": "/api/status",
        "queryUrl": "/api/query",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)
