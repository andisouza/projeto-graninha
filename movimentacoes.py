import json
import os
from datetime import date, datetime
from uuid import uuid4

MOVIMENTACOES_FILE = "data/movimentacoes.json"


def carregar_movimentacoes():
    """
    Carrega todas as movimentações do arquivo JSON.

    Returns:
        list: Lista de dicionários com as movimentações
              Lista vazia se o arquivo não existir ou estiver corrompido."""

    if not os.path.exists(MOVIMENTACOES_FILE):
        return []
    with open(MOVIMENTACOES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_movimentacoes(movimentacoes):
    """
    Salva a lista de movimentações no arquivo JSON.

    Args:
        movimentacoes (list): Lista de dicionários de movimentações.
    """

    with open(MOVIMENTACOES_FILE, "w", encoding="utf-8") as f:
        json.dump(movimentacoes, f, indent=4, ensure_ascii=False)


def movimentacao(email, tipo, valor, categoria, descricao="", data=None):
    """
    Adiciona uma entrada de saldo.
    """

    if tipo not in ["entrada", "saida"]:
        return {"sucesso": False, "mensagem": "Tipo de movimentação inválida"}

    if data is None:
        data = date.today().isoformat()

    movimentacoes = carregar_movimentacoes()

    movimentacao = {
        "id": str(uuid4()),
        "email": email,
        "tipo": tipo,
        "valor": valor,
        "categoria": categoria,
        "descricao": descricao,
        "data": data,
    }

    movimentacoes.append(movimentacao)
    salvar_movimentacoes(movimentacoes)

    return {
        "sucesso": True,
        "mensagem": (f"{tipo.capitalize()} adicionada com sucesso!"),
    }


def listar_movimentacoes(email):
    """
    Lista todas as movimentações do usuário.
    """

    movimentacoes = carregar_movimentacoes()
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

    movimentacoes = carregar_movimentacoes()
    novas_movs = [
        m for m in movimentacoes if not (m["id"] == mov_id and m["email"] == email)
    ]

    if len(novas_movs) < len(movimentacoes):
        salvar_movimentacoes(novas_movs)
        return {"sucesso": True, "mensagem": "Movimentação removida com sucesso!"}
    else:
        return {"sucesso": False, "mensagem": "Movimentação não encontrada."}
