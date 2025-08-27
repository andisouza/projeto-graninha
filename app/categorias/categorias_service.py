from app.utils import carregar_json, salvar_json, gerar_id


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
    usuario_categs = [c for c in categorias_usuario if c["email"] == email]

    categorias_do_usuario = [c["categoria"] for c in usuario_categs]

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

    usuario_categs = [c for c in categorias_usuario if c["email"] == email]
    categoria_a_remover = next((c for c in usuario_categs if c["id"] == categ_id), None)

    if not categoria_a_remover:
        return {"sucesso": False, "mensagem": "Categoria não encontrada."}

    novas_categs = [c for c in categorias_usuario if c != categoria_a_remover]

    salvar_json(CATEGORIAS_USUARIO_FILE, novas_categs)
    return {"sucesso": True, "mensagem": "Categoria removida com sucesso!"}
