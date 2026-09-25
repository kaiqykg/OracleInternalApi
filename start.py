"""Script de inicialização da API Oracle Internal (PCM)"""
import sys
import uvicorn
from core.config import HOST, PORT

def run():
    print("=" * 60)
    print("   Iniciando OracleInternalApi (FastAPI + Thick Mode)")
    print(f"   Acessivel em: http://{HOST}:{PORT}")
    print(f"   Documentacao: http://localhost:{PORT}/docs")
    print("=" * 60)
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)

if __name__ == "__main__":
    run()
