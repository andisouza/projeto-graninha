from fastapi import APIRouter
from app.login.login_service import cadastrar_usuario, login

login_router = APIRouter(prefix="/login", tags=["Login"])


@login_router.post("/cadastrar")
def endpoint_cadastrar(nome: str, email: str, data_nasc: str, senha: str):
    return cadastrar_usuario(nome, email, data_nasc, senha)


@login_router.post("/")
def endpoint_login(email: str, senha: str):
    return login(email, senha)
