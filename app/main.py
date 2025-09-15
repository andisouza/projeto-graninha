from fastapi import FastAPI

# from app.usuarios import usuarios_router
from app.movimentacoes.movimentacoes_router import movimentacoes_router
from app.auth.auth_router import auth_router
from app.categorias.categorias_router import categorias_router

app = FastAPI(title="Projeto Graninha", version="1.0")

# app.include_router(usuarios_router)
app.include_router(movimentacoes_router)
app.include_router(auth_router)
app.include_router(categorias_router)
