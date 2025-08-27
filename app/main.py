from fastapi import FastAPI

# from app.usuarios import usuarios_router
from app.movimentacoes import movimentacoes_router
from app.login import login_router
from app.categorias import categorias_router

app = FastAPI(title="Projeto Graninha", version="1.0")

# app.include_router(usuarios_router)
app.include_router(movimentacoes_router)
app.include_router(login_router)
app.include_router(categorias_router)
