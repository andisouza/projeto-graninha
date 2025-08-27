from fastapi import APIRouter
from app.movimentacoes.movimentacoes_service import (
    listar_movimentacoes,
    movimentacao,
    remover_movimentacao,
    calcular_saldo,
    movimentacoes_por_categoria,
    movimentacoes_por_periodo,
)

movimentacoes_router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@movimentacoes_router.post("/adicionar")
def adicionar_movimentacao(
    email: str,
    tipo: str,
    valor: float,
    categoria: str,
    descricao: str = "",
    data: str | None = None,
):
    resultado = movimentacao(email, tipo, valor, categoria, descricao, data)
    return resultado


@movimentacoes_router.get("/")
def listar_movs(
    email: str,
    categoria: str | None = None,
    inicio: str | None = None,
    fim: str | None = None,
):
    # sem filtros
    if not categoria and not (inicio and fim):
        movs = listar_movimentacoes(email)
        return {"sucesso": True, "dados": movs}

    # filtro por categ
    if categoria:
        movs = movimentacoes_por_categoria(email, categoria)
        return {"sucesso": True, "dados": movs}

    # filtro por periodo
    if inicio and fim:
        movs = movimentacoes_por_periodo(email, inicio, fim)
        return {"sucesso": True, "dados": movs}

    return {"sucesso": False, "mensagem": "Parâmetros de filtro inválidos."}


@movimentacoes_router.get("/saldo")
def saldo(email: str):
    saldo_atual = calcular_saldo(email)
    return {"sucesso": True, "dados": {"saldo": saldo_atual}}


@movimentacoes_router.delete("/remover/{mov_id}")
def remover(email: str, mov_id: str):
    resultado = remover_movimentacao(email, mov_id)
    return resultado
