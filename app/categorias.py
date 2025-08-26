from utils import carregar_json, salvar_json, gerar_id

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


def listar_categorias(email):
    """
    Lista todas as categorias do usuário.
    """

    categorias_usuario = carregar_json(CATEGORIAS_USUARIO_FILE)
    usuario = next((c for c in categorias_usuario if c["email"] == email), None)
    return usuario["categorias"] if usuario else CATEGORIAS


def adicionar_categoria(email, nova_categoria):
    """
    Adiciona a categoria do usuário no arquivo.

    Returns:
        dict: {"sucesso"}: bool, "mensagem": str}
    """

    categorias_usuario = carregar_json(CATEGORIAS_USUARIO_FILE)

    # Verifica se já existe a categoria
    categorias_do_usuario = [
        c["categoria"] for c in categorias_usuario if c["email"] == email
    ]

    if nova_categoria in categorias_do_usuario:
        return {"sucesso": False, "mensagem": "Categoria já existente"}

    # Add nova categoria com ID
    nova = {"id": gerar_id(), "email": email, "categoria": nova_categoria}
    categorias_usuario.append(nova)
    salvar_json(CATEGORIAS_USUARIO_FILE, categorias_usuario)

    return {"sucesso": True, "mensagem": "Categoria adicionada com sucesso!"}


def remover_categoria(email, categ_id):
    """
    Remove uma categoria pelo id.
    """

    categorias_usuario = carregar_json(CATEGORIAS_USUARIO_FILE)
    novas_categs = [
        c
        for c in categorias_usuario
        if not (c["id"] == categ_id and c["email"] == email)
    ]

    if len(novas_categs) < len(categorias_usuario):
        salvar_json(CATEGORIAS_USUARIO_FILE, novas_categs)
        return {"sucesso": True, "mensagem": "Categoria removida com sucesso!"}
    else:
        return {"sucesso": False, "mensagem": "Categoria não encontrada."}
