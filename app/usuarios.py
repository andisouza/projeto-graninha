from fastapi import APIRouter

router = APIRouter()


@router.get("/teste")
def teste():
    return {"mensagem": "Funciona"}
