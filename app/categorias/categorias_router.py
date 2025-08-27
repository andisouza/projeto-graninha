from fastapi import APIRouter
from app.categorias.categorias_service import adicionar_categoria

categorias_router = APIRouter(prefix="/categorias", tags=["Categorias"])


@categorias_router.post("/adicionar")
def endpoint_adicionar_categoria(email: str, nova_categoria: str):
    return adicionar_categoria(email, nova_categoria)
