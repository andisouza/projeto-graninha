from app.utils import carregar_json, salvar_json, gerar_id
from datetime import date, datetime

MOVIMENTACOES_FILE = "data/movimentacoes.json"


def movimentacao(email, tipo, valor, categoria, descricao="", data=None):
    """
    Adiciona uma entrada de saldo.
    """

    if tipo not in ["entrada", "saida"]:
        return {"sucesso": False, "mensagem": "Tipo de movimentação inválida"}

    if data is None:
        data = date.today().isoformat()

    movimentacoes = carregar_json(MOVIMENTACOES_FILE)

    movimentacao = {
        "id": gerar_id(),
        "email": email,
        "tipo": tipo,
        "valor": valor,
        "categoria": categoria,
        "descricao": descricao,
        "data": data,
    }

    movimentacoes.append(movimentacao)
    salvar_json(MOVIMENTACOES_FILE, movimentacoes)

    return {
        "sucesso": True,
        "mensagem": (f"{tipo.capitalize()} adicionada com sucesso!"),
    }


def listar_movimentacoes(email):
    """
    Lista todas as movimentações do usuário.
    """

    movimentacoes = carregar_json(MOVIMENTACOES_FILE)
    return [m for m in movimentacoes if m["email"] == email]


def calcular_saldo(email):
    """
    Soma as entradas e subtrai as saídas.
    """

    movimentacoes = listar_movimentacoes(email)

    saldo = sum(
        m["valor"] if m["tipo"] == "entrada" else -m["valor"] for m in movimentacoes
    )
    return saldo


def movimentacoes_por_categoria(email, categoria):
    """
    Retorna as movimentações do usuário com filtro por categoria.

    Returns:
        list: lista de dicionários com as movs da categoria."""

    usuario_movs = listar_movimentacoes(email)
    return [m for m in usuario_movs if m["categoria"] == categoria]


def movimentacoes_por_periodo(email, inicio, fim):
    """
    Retorna as movimentações do usuário no período escolhido.

    Args:
        email (str): email do usuário
        inicio (str): data inicial
        fim (str): data final

    Returns:
        list: lista de dicionários com as movs do período.
    """

    usuario_movs = listar_movimentacoes(email)

    inicio_date = datetime.strptime(inicio, "%Y-%m-%d").date()
    fim_date = datetime.strptime(fim, "%Y-%m-%d").date()

    return [
        m
        for m in usuario_movs
        if inicio_date <= datetime.strptime(m["data"], "%Y-%m-%d").date() <= fim_date
    ]


def remover_movimentacao(email, mov_id):
    """
    Remove uma movimentação pelo id.
    """

    movimentacoes = carregar_json(MOVIMENTACOES_FILE)
    novas_movs = [
        m for m in movimentacoes if not (m["id"] == mov_id and m["email"] == email)
    ]

    if len(novas_movs) < len(movimentacoes):
        salvar_json(MOVIMENTACOES_FILE, novas_movs)
        return {"sucesso": True, "mensagem": "Movimentação removida com sucesso!"}
    else:
        return {"sucesso": False, "mensagem": "Movimentação não encontrada."}
