from fastapi import APIRouter
from app.auth.auth_service import cadastrar_usuario, login

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/cadastrar")
async def endpoint_cadastrar(nome: str, email: str, data_nasc: str, senha: str):
    return cadastrar_usuario(nome, email, data_nasc, senha)


@auth_router.post("/login")
def endpoint_login(email: str, senha: str):
    return login(email, senha)
