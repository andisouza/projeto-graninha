from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Date,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão do banco
db = create_engine("sqlite:///data/banco.db")
# Aqui futuramente vem a url do db

# Cria a base do banco de dados
Base = declarative_base()


# Classes/tabelas do BD
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True, index=True)
    data_nasc = Column("data de nascimento", Date, nullable=False)
    senha = Column("senha", String, nullable=False)

    def __init__(self, nome, email, data_nasc, senha):
        self.nome = nome
        self.email = email
        self.data_nasc = data_nasc
        self.senha = senha


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    # TIPO_MOVIMENTACAO = (("ENTRADA", "ENTRADA"), ("SAIDA", "SAIDA"))

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"))
    descricao = Column("descrição", String, nullable=False)
    valor = Column("valor", Float, nullable=False)
    tipo = Column("tipo", String, nullable=False)
    data = Column("data", DateTime, default=func.now(), nullable=False)

    def __init__(self, descricao, valor, tipo):
        self.descricao = descricao
        self.valor = valor
        self.tipo = tipo


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"), nullable=True)

    def __init__(self, nome, usuario_id=None):
        self.nome = nome
        self.usuario_id = usuario_id


# executa a criação dos metadados (cria efetivamente o bd)


#    def add_transacao(self, transacao):
#        self.transacoes.append(transacao)

#    def calcular_saldo(self):
#        saldo = 0
#        for t in self.transacoes:
#            if t["tipo"] == "receita":
#                saldo += t["valor"]
#            else:
#                saldo -= t["valor"]
#        return saldo#

#    def listar_historico(self):
#        return self.transacoes

#    def to_dict(self):
#        return {
#            "nome": self.nome,
#            "email": self.email,
#            "data_nasc": self.data_nasc,
#            "senha": self.senha,
#            "transacoes": self.transacoes,
#
