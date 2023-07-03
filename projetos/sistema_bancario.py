#funções
def depositar(deposito, saldo, extrato, /):
    if deposito > 0:
        saldo += deposito
        print('Depósito realizado com sucesso!')
        extrato += f"Depósito R${deposito:.2f} \n"
    else:
        print('Não é possivel depositar valores negativos!')
    return saldo, extrato

def sacar(*, saldo, valor_saque, extrato, limite, numero_saques):
    if valor_saque <= 0 :
        print('Não foi possível realizar o saque. Valor inválido')
    elif valor_saque > saldo:
        print('Não foi possível realizar o saque. Saldo insuficiente')
    elif valor_saque > limite:
        print('Não foi possível realizar o saque. Valor da operação maior que o permitido!')
    else:
        saldo -= valor_saque
        numero_saques +=1
        print('Saque realizado com sucesso!')
        extrato += f"Saque R${valor_saque:.2f} \n"
    return saldo, extrato, numero_saques

def visualizar_extrato(saldo, /, *, extrato):
    print("######## EXTRATO ########")
    print(extrato)
    print(f'Saldo: R${saldo:.2f}')
    print("#########################")

def criar_novo_usuario(lista_usuarios):
    cpf = input('Digite seu CPF (somente números): ')

    for conta in lista_usuarios:
        if cpf == conta['cpf']:
            print('Usuário já cadastrado no banco')
            return

    nome = input('Digite seu nome completo: ')
    data_nascimento = input('Digite sua data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite seu endereço (logradouro, nº - bairro - cidade/sigla estado): ')
    usuario_dict = {'cpf': cpf, 'nome':nome, 'data_nascimento':data_nascimento, 'endereco': endereco}
    lista_usuarios.append(usuario_dict)
    print('Usuário cadastrado com sucesso!')

def criar_nova_conta(agencia, numero_conta, lista_usuarios, lista_conta):
    cpf = input('Digite o CPF do cliente (apenas números): ')

    for conta in lista_usuarios:
        if cpf == conta['cpf']:
            print('Conta criada com sucesso!')
            lista_conta.append({'numero_conta': numero_conta, 'agencia': agencia, 'usuario': conta['nome']})
            return
    else:
        print('Usuário não encontrado!')

def listar_usuarios(lista_usuarios):
    print('*****LISTA DE USUÁRIOS*****\n')
    for conta in lista_usuarios:
        print(f"CPF: {conta['cpf']} Nome: {conta['nome']} Data de nascimento: {conta['data_nascimento']} Logradouro: {conta['endereco']}")
    print("\n***************************")

def listar_contas(lista_contas):
    print('*****LISTA DE CONTAS*****\n')
    for conta in lista_contas:
        print(f"Conta {conta['numero_conta']}: Agência {conta['agencia']} Titular: {conta['usuario']}")
    print("\n*************************")

#Variaveis
extrato = ""
numero_saques = 0
saldo = 0
lista_usuarios = []
lista_contas = []
LIMITE_SAQUE_DIARIO = 3
LIMITE_MAXIMO_SAQUE = 500
AGENCIA = '0001'


display ="""

Bem- Vindo(a)

[u] Novo usuário
[c] Nova Conta
[lu] Listar Usuários
[lc] Listar Contas
[d] Realizar depósito
[s] Realizar saque
[e] Verificar extrato
[q] Sair do sistema

 """

while True:
    opcao_usuario = input(display)

    if opcao_usuario == 'd':
        deposito = int(input('Digite o valor que deseja depoistar: '))
        saldo, extrato = depositar(deposito, saldo, extrato)
    
    elif opcao_usuario == 's':
        if numero_saques < LIMITE_SAQUE_DIARIO:
            valor_saque = int(input('Digite o valor que deseja sacar: '))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor_saque=valor_saque, extrato=extrato, limite=LIMITE_MAXIMO_SAQUE, numero_saques=numero_saques)
        else:
            print('Limite máximo de saques diários atingido!')
    
    elif opcao_usuario == 'e':
        visualizar_extrato(saldo, extrato=extrato)
    
    elif opcao_usuario == 'q':
        break

    elif opcao_usuario == 'u':
        criar_novo_usuario(lista_usuarios)
    
    elif opcao_usuario == 'lu':
        listar_usuarios(lista_usuarios)

    elif opcao_usuario == 'lc':
        listar_contas(lista_contas)

    elif opcao_usuario == 'c':
        criar_nova_conta(AGENCIA, len(lista_contas)+1, lista_usuarios, lista_contas)

    else:
        print('Opção inválida! Por favor, digite novamente a opção desejada.')