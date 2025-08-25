import json
import os
import bcrypt

from api.validacoes import (
    validar_nome,
    validar_email,
    validar_data_nasc,
    validar_senha,
)

USUARIOS_FILE = "data/usuarios.json"


class Usuario:
    def __init__(self, nome, email, data_nasc, senha):
        self.nome = nome
        self.email = email
        self.data_nasc = data_nasc
        self.senha = senha
        self.transacoes = []  # Lista de transações do usuário

    def add_transacao(self, transacao):
        self.transacoes.append(transacao)

    def calcular_saldo(self):
        saldo = 0
        for t in self.transacoes:
            if t["tipo"] == "receita":
                saldo += t["valor"]
            else:
                saldo -= t["valor"]
        return saldo

    def listar_historico(self):
        return self.transacoes

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "data_nasc": self.data_nasc,
            "senha": self.senha,
            "transacoes": self.transacoes,
        }


def carregar_usuarios():
    """
    Carrega todos os usuários do arquivo JSON.

    Returns:
        list: Lista de dicionários com os usuários cadastrados.
              Lista vazia se o arquivo não existir ou estiver corrompido."""

    if not os.path.exists(USUARIOS_FILE):
        return []
    with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo JSON.

    Parâmetros:
        usuarios (list): Lista de dicionários de usuários.
    """

    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


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


def add_usuario(usuario_dict):
    """
    Adiciona um usuário na base de dados JSON.

    Parâmetros:
        usuario_dict (dict): Dicionário com os dados do usuário."""

    usuarios = carregar_usuarios()
    usuarios.append(usuario_dict)
    salvar_usuarios(usuarios)


def usuario_publico(usuario_dict):
    """Retorna apenas os dados públicos do usuário, sem a senha."""
    return {k: v for k, v in usuario_dict.items() if k != "senha"}


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

    if usuario:
        senha_bytes = senha.encode()
        if bcrypt.checkpw(senha_bytes, usuario["senha"].encode()):
            return {
                "sucesso": True,
                "mensagem": "Login realizado com sucesso",
                "usuario": usuario_publico(usuario),
            }
        else:
            return {"sucesso": False, "mensagem": "Senha incorreta"}

    return {"sucesso": False, "mensagem": "Email ou senha incorretos"}
