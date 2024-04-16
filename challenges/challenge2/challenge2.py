from abc import ABC, abstractmethod
import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001"
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > self.saldo:
            return False
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saques):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):

        num_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        if num_saques <= self.limite_saques:
            return False
        elif valor > self.limite:
            return False
        else:
            return super().sacar(valor)
    
    def __str__(self):
        return f"{self.agencia}, {self.numero}, {self.cliente.nome}"

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Transacao(ABC):
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao = conta.depositar(self.valor)

        if transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao = conta.sacar(self.valor)

        if transacao:
            conta.historico.adicionar_transacao(self)

class Historico():
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )
