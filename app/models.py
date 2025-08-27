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
