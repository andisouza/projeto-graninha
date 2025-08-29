from fastapi import FastAPI

# from app.usuarios import usuarios_router
from app.movimentacoes.movimentacoes_router import movimentacoes_router
from app.login.login_router import login_router
from app.categorias.categorias_router import categorias_router

app = FastAPI(title="Projeto Graninha", version="1.0")

# app.include_router(usuarios_router)
app.include_router(movimentacoes_router)
app.include_router(login_router)
app.include_router(categorias_router)
