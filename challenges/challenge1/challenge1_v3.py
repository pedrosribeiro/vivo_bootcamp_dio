import os
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

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
            print("Valor maior que o saldo da conta!")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("Saque efetuado com sucesso!")
            return True
        else:
            print("Não foi possível sacar!")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito efetuado com sucesso!")
            return True
        else:
            print("Não foi possível depositar!")
            return False

# iterador
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return conta
        except IndexError:
            raise StopIteration

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
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

        if num_saques > self.limite_saques:
            print("Limite de saques atingido!")
            return False
        elif valor > self.limite:
            print("Valor maior que o limite da conta!")
            return False
        else:
            return super().sacar(valor)
    
    def __str__(self):
        return f"Agência: {self.agencia}, Conta: {self.numero}, Titular: {self.cliente.nome}"

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self._contas = []
    
    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Limite de transações diárias excedidas!")
            return
            
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )
    
    # gerador
    def gerar_relatorio(self):
        for transacao in self._transacoes:
            yield transacao
    
    def transacoes_do_dia(self):
        data_atual = datetime.now()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

def clear_console():
    os.system("cls")

def filtrar_cliente(cpf, clientes):

    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]

    return cliente[0] if cliente else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return

    n_conta = int(input(f"Insira o número da conta: {[i for i in range(len(cliente.contas))]}: "))
    
    return cliente.contas[n_conta]

# função decoradora
def log_transacao(func):
    def envelope(*args, **kwargs):
        func(*args)
        print(func.__name__, datetime.now())
    
    return envelope

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    valor = float(input("Quanto deseja depositar?"))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    valor = float(input("Quanto deseja sacar?"))
    transacao = Saque(valor)
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n========== EXTRATO ==========\n")
    extrato = ""
    movimentacoes = False

    for transacao in conta.historico.gerar_relatorio():
        movimentacoes = True
        extrato += f"{transacao['data']} {transacao['tipo']}: R$ {transacao['valor']:.2f}\n"

    if not movimentacoes:
        extrato = "Nenhuma operação realizada!\n"

    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}\n")
    print("=============================\n")

@log_transacao
def criar_cliente(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Usuário já cadastrado!")
        return

    name = input("Informe o nome: ")
    birth_date = input("Informe a data de nascimento (dd/mm/aa): ")
    address = input("Informe o endereço (rua, número - bairro - cidade/UF): ")

    cliente = PessoaFisica(cpf, name, birth_date, address)

    clientes.append(cliente)

@log_transacao
def criar_conta(numero_conta, clientes, contas):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado!")
        return
    
    conta = ContaCorrente(numero_conta, cliente, 500, 3)
    contas.append(conta)
    cliente.adicionar_conta(conta)

def listar_contas(contas):
    for conta in ContaIterador(contas):
        print("======================")
        print(textwrap.dedent(str(conta)))
        print("======================")

def menu():
    menu = """
        Escolha a operação que deseja realizar

        [d] Depósito
        [s] Saque
        [e] Extrato
        [nu] Novo cliente
        [nc] Nova conta
        [lc] Listar contas

        [q] Sair
    """

    return input(menu)

def main():
    clientes = []
    contas = []

    while True:

        option = menu()

        if option == "d":
            depositar(clientes)
        elif option == "s":
            sacar(clientes)
        elif option == "e":
            exibir_extrato(clientes)
        elif option == "nu":
            criar_cliente(clientes)
        elif option == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif option == "lc":
            listar_contas(contas)
        elif option == "q":
            print("Saindo...")
            break
        else:
            print("Operação inválida!")

if __name__ == "__main__":
    main()