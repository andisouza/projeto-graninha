from fastapi import FastAPI
from app import usuarios, movimentacoes, categorias

app = FastAPI(title="Projeto Graninha", version="1.0")

# Endpoints de cada módulo
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(
    movimentacoes.router, prefix="/movimentacoes", tags=["Movimentações"]
)
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
