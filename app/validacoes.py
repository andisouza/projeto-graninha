import re
from datetime import datetime


def validar_nome(nome):
    """
    Verifica se o nome é válido.

    Parâmetros:
        nome (str): Nome do usuário

    Retorna:
        bool: True se o nome for válido, False caso contrário."""

    padrao = r"^[A-Za-zÀ-ÿ]+(?: [A-Za-zÀ-ÿ]+)*$"
    return bool(re.match(padrao, nome))


def validar_email(email):
    """
    Valida se é um e-mail válido, com @ e .

    Parâmetros:
        email (str): Email do usuário

    Retorna:
        bool: True se o email for válido, False caso contrário."""

    padrao = r"^([a-zA-Z._-\d]{1,})[@]([a-zA-Z0-9.-]{2,})[.]([a-zA-Z]{2,})$"
    return bool(re.match(padrao, email))


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

    padrao = (
        r"^(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@$!%*?&])"
        r"[A-Za-z\d@$!%*?&]{8,20}$"
    )
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
