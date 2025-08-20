import re
from datetime import datetime

usuarios = []


class Usuario:
    def __init__(self, nome, email, data_nasc, senha):
        self.nome = nome
        self.email = email
        self.data_nasc = data_nasc
        self.senha = senha
        self.transacoes = []  # Lista para guardar as transações do usuário

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


def validar_nome(nome):
    return nome.strip() != ""


def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def validar_senha(senha):
    """
    Valida se a senha cumpre todos os requisitos.
    - 8 a 20 caracteres
    - Pelo menos 1 letra maíscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 caractere especial (@$!%*?&)
    - Pelo menos 1 número
    - Não conter só espaços

    Parâmetros:
        senha (str): Senha escolhida pelo usuário

    Retorna:
        bool: True se a senha for válida, False caso contrário."""

    padrao = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
    return bool(re.match(padrao, senha))


def validar_data_nasc(data_nasc):
    """
    Valida se a data não está no futuro e se está entre 18 a 110 anos.

    Parâmetros:
        data_nasc (str): Data de nascimento do usuário

    Retorna:
        bool: True se a data for válida, False caso contrário."""

    try:
        data = datetime.strptime(data_nasc, "%d/%m/%Y")
        hoje = datetime.now()

        # Verifica se não está no futuro
        if data > hoje:
            return False

        # Idade aprox.
        idade = (hoje - data).days // 365

        # Limite de idade
        if idade < 18 or idade > 110:
            return False

        return True
    except ValueError:
        return False


def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    senha = input("Senha: ")

    for u in usuarios:
        if u.email == email:
            print("Email já cadastrado!")
            return None

    usuario = Usuario(nome, email, data_nasc, senha)
    usuarios.append(usuario)
    print(f"Usuario {nome} cadastrado com sucesso!")
    return usuario


def login():
    email = input("Email: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u.email == email and u.senha == senha:
            print("Bem vindo!")
            return u

    print("Email ou senha incorretos!")
    return None


def menu():
    while True:
        print("\n1 - Cadastrar usuário")
        print("2 - Login")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastrar_usuario()
        elif escolha == "2":
            user = login()
            if user:
                print(f"Saldo atual: {user.calcular_saldo()}")
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


menu()
