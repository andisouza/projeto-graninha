from app.utils import carregar_json, salvar_json
import bcrypt
from app.models import Usuario

from app.validacoes import (
    validar_nome,
    validar_email,
    validar_data_nasc,
    validar_senha,
)


USUARIOS_FILE = "data/usuarios.json"


def carregar_usuarios():
    """
    Carrega todos os usuários do arquivo JSON."""

    return carregar_json(USUARIOS_FILE)


def salvar_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo JSON.
    """

    salvar_json(USUARIOS_FILE, usuarios)


def add_usuario(usuario_dict):
    """
    Adiciona um usuário na base de dados JSON.

    Parâmetros:
        usuario_dict (dict): Dicionário com os dados do usuário."""

    usuarios = carregar_usuarios()
    usuarios.append(usuario_dict)
    salvar_usuarios(usuarios)


def cadastrar_usuario(nome, email, data_nasc, senha):
    """
    Valida dados, aplica hash de senha, cria o usuário
    e salva no JSON.

    Parâmetros:
        nome (str)
        email (str)
        data_nasc (str)
        senha (str)

    Returns:
        dict: { "sucesso": bool, "mensagem": str}
    """

    # Validações
    if not validar_nome(nome):
        return {"sucesso": False, "mensagem": "Nome inválido"}

    if not validar_email(email):
        return {"sucesso": False, "mensagem": "Email inválido"}

    usuarios = carregar_usuarios()
    if any(u["email"] == email for u in usuarios):
        return {"sucesso": False, "mensagem": "Email já cadastrado"}

    if not validar_data_nasc(data_nasc):
        return {"sucesso": False, "mensagem": "Data de nascimento inválida"}

    if not validar_senha(senha):
        return {"sucesso": False, "mensagem": "Senha inválida"}

    # Hash de senha
    senha_bytes = senha.encode()  # transforma em bytes
    hashed = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    senha_hashed_str = hashed.decode()  # transforma em string pra salvar

    # Cria o usuário
    usuario = Usuario(nome, email, data_nasc, senha_hashed_str)

    # Salva nos dados
    add_usuario(usuario.to_dict())

    # Retorno de sucesso
    return {
        "sucesso": True,
        "mensagem": (f"Usuário {nome} cadastrado com sucesso!"),
    }


def login(email, senha):
    """
    Verifica se o email e senha correspondem
    a algum usuário cadastrado.

    Parâmetros:
        email (str)
        senha (str)

    Returns:
        dict: {"sucesso": bool, "mensagem": str, "usuario": dict}
    """

    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u["email"] == email), None)

    if not usuario:
        return {"sucesso": False, "mensagem": "Email ou senha incorretos"}

    if not bcrypt.checkpw(senha.encode(), usuario["senha"].encode()):
        return {"sucesso": False, "mensagem": "Senha incorreta"}

    # Retorna dados públicos
    return {
        "sucesso": True,
        "mensagem": "Login realizado com sucesso",
        "usuario": {k: v for k, v in usuario.items() if k != "senha"},
    }


def usuario_publico(usuario_dict):
    """Retorna apenas os dados públicos do usuário, sem a senha."""
    return {k: v for k, v in usuario_dict.items() if k != "senha"}
