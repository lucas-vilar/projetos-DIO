from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, nova_conta):
        self.contas.append(nova_conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente, agencia='0001', saldo=0):
        self._numero = numero
        self._cliente = cliente
        self._agencia = agencia
        self._saldo = saldo
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def realizar_saque(self, valor_saque):
        saldo = self._saldo

        if valor_saque > saldo:
            print('\nNão foi possível realizar o saque. Valor insuficiente!')
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print('\nSaque realizado com sucesso!')
            return True
        else:
            print('Não foi possível realizar o saque. Valor inválido!')
        
        return False

    def realizar_deposito(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print('Depósito realizado com sucesso!')
        else:
            print('Não foi possível realizar o depósito. Valor inválido!')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia='0001', saldo=0, limite_valor=500, limite_saques=3):
        super().__init__(numero, cliente, agencia, saldo)
        self._limite_valor = limite_valor
        self._limite_saques = limite_saques

    def realizar_saque(self, valor_saque):
        numero_saques = len( [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__] )

        if valor_saque > self._limite_valor:
            print('Não foi possível realizar o saque. Valor acima do permitido!')

        elif numero_saques >= self._limite_saques:
            print('Não foi possível realizar o saque. Limite de saques excedido!')
        
        else:
            return super().realizar_saque(valor_saque)
    
        return False
        
    def __str__(self):
        return f"""
            Agência: {self._agencia}
            Conta Corrente: {self._numero}
            Titular: {self._cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def nova_transicao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor, "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")})

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_efetuada = conta.realizar_saque(self._valor)

        if transacao_efetuada:
            conta.historico.nova_transicao(self)

class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_efetuada = conta.realizar_deposito(self._valor)

        if transacao_efetuada:
            conta.historico.nova_transicao(self)

#funções
def depositar(lista_cliente):
    cpf = input('Digite o CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, lista_cliente)

    if not cliente:
        print("Cliente não encontrado no sistema!")
        return
    
    valor_deposito = int(input("Informe o valor do depósito: "))
    transacao = Deposito(valor_deposito)

    conta  = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, lista_clientes):
    clientes_filtrados = [cliente for cliente in lista_clientes if cliente.cpf == cpf]
    
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("O cliente não possui conta!")
        return
    return cliente.contas[0]

def sacar(lista_clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, lista_clientes)

    if not cliente:
        print("Cliente não encontrado no sistema!")
        return
    
    valor_saque = int(input("Digite o valor do saque: "))
    transacao = Saque(valor_saque)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    cliente.realizar_transacao(conta, transacao)

def visualizar_extrato(lista_clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, lista_clientes)

    if not cliente:
        print("Cliente não encontrado no sistema!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    print("------------EXTRATO------------")
    lista_transacoes = conta.historico.transacoes

    extrato = ""
    if not lista_transacoes:
        extrato = "Não foram encontradas transações nessa conta!"
    else:
        for transacao in lista_transacoes:
            extrato += f"Transação: {transacao['tipo']}     Valor: R${transacao['valor']:.2f}\n\n"
    print(extrato)
    print(f"Saldo: R${conta.saldo:.2f}\n")
    print("---------------------------------")

def criar_novo_cliente(lista_clientes):
    cpf = input('Digite o CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, lista_clientes)

    if cliente:
        print('\nCliente já cadastrado!')

    nome = input('Digite o nome completo do cliente: ')
    data_nascimento = input('Digite a data de nascimento (dd-mm-aaaa) do cliente: ')
    endereco = input('Digite o endereço (logradouro, nº - bairro - cidade/sigla estado) do cliente: ')
    
    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    lista_clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")

def criar_nova_conta(numero_conta, lista_clientes, lista_conta):
    cpf = input('Digite o CPF do cliente (apenas números): ')
    cliente = filtrar_cliente(cpf, lista_clientes)

    if not cliente:
        print('Cliente não encontrado no sistema!')
        return
    
    conta = ContaCorrente.nova_conta(numero_conta, cliente)
    lista_conta.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(lista_contas):
    print('----------LISTA DE CONTAS----------\n')
    for conta in lista_contas:
        print(str(conta))
        print("")
    print("\n*************************")

def display():
    display ="""

********Bem- Vindo(a)********
*                           *
*    [u] Novo Cliente       *
*    [c] Nova Conta         *
*    [lc] Listar Contas     *
*    [d] Realizar depósito  *
*    [s] Realizar saque     *
*    [e] Verificar extrato  *
*    [q] Sair do sistema    *
*                           *
*****************************
 """
    return input(display)

def main():
    lista_clientes = []
    lista_contas = []

    while True:
        opcao_usuario = display()

        if opcao_usuario == 'd':
            depositar(lista_clientes)
        
        elif opcao_usuario == 's':
            sacar(lista_clientes)
        
        elif opcao_usuario == 'e':
            visualizar_extrato(lista_clientes)
        
        elif opcao_usuario == 'q':
            break

        elif opcao_usuario == 'u':
            criar_novo_cliente(lista_clientes)

        elif opcao_usuario == 'lc':
            listar_contas(lista_contas)

        elif opcao_usuario == 'c':
            n_contas = len(lista_contas)+1
            criar_nova_conta(n_contas, lista_clientes, lista_contas)

        else:
            print('Opção inválida! Por favor, digite novamente a opção desejada.')

main()