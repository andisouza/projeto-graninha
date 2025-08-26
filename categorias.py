import json
import os
from uuid import uuid4

CATEGORIAS = [
    "Alimentação",
    "Transporte",
    "Saúde",
    "Lazer",
    "Educação",
    "Moradia",
    "Outros",
]

CATEGORIAS_USUARIO_FILE = "data/categorias_usuario.json"


def carregar_categorias_usuario():
    """
    Carrega as categorias do arquivo JSON.

    Returns:
        list: Lista de dicionários com as categorias
              Lista vazia se o arquivo não existir ou estiver corrompido."""

    if not os.path.exists(CATEGORIAS_USUARIO_FILE):
        return []
    with open(CATEGORIAS_USUARIO_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_categorias_usuario(categorias):
    """
    Salva a lista de categorias no arquivo JSON.

    Args:
        categorias (list): Lista de dicionários de categorias.
    """

    with open(CATEGORIAS_USUARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(categorias, f, indent=4, ensure_ascii=False)


def listar_categorias(email):
    """
    Lista todas as categorias do usuário.
    """

    categorias_usuario = carregar_categorias_usuario()
    usuario = next((c for c in categorias_usuario if c["email"] == email), None)
    return usuario["categorias"] if usuario else CATEGORIAS


def adicionar_categoria(email, nova_categoria):
    """
    Adiciona a categoria do usuário no arquivo.

    Returns:
        dict: {"sucesso"}: bool, "mensagem": str}
    """

    categorias_usuario = carregar_categorias_usuario()

    # Verifica se já existe a categoria
    categorias_do_usuario = [
        c["categoria"] for c in categorias_usuario if c["email"] == email
    ]

    if nova_categoria in categorias_do_usuario:
        return {"sucesso": False, "mensagem": "Categoria já existente"}

    # Add nova categoria com ID
    nova = {"id": str(uuid4()), "email": email, "categoria": nova_categoria}
    categorias_usuario.append(nova)
    salvar_categorias_usuario(categorias_usuario)

    return {"sucesso": True, "mensagem": "Categoria adicionada com sucesso!"}


def remover_categoria(email, categ_id):
    """
    Remove uma categoria pelo id.
    """

    categorias_usuario = carregar_categorias_usuario()
    novas_categs = [
        c
        for c in categorias_usuario
        if not (c["id"] == categ_id and c["email"] == email)
    ]

    if len(novas_categs) < len(categorias_usuario):
        salvar_categorias_usuario(novas_categs)
        return {"sucesso": True, "mensagem": "Categoria removida com sucesso!"}
    else:
        return {"sucesso": False, "mensagem": "Categoria não encontrada."}
