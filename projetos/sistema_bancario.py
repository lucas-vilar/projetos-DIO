#Variaveis

extrato = ""

numero_saques = 0

LIMITE_SAQUE_DIARIO = 3

LIMITE_MAXIMO_SAQUE = 500

saldo = 0

display ="""

Bem- Vindo(a)

[d] Realizar depósito
[s] Realizar saque
[e] Verificar extrato
[q] Sair do sistema

 """

while True:
    opcao_usuario = input(display)

    if opcao_usuario == 'd':
        deposito = int(input('Digite o valor que deseja depoistar: '))
        if deposito > 0:
            saldo += deposito
            print('Depósito realizado com sucesso!')
            extrato += f"Depósito R${deposito:.2f} \n"
        else:
            print('Não é possivel depositar valores negativos!')
    
    elif opcao_usuario == 's':
        if numero_saques < LIMITE_SAQUE_DIARIO:
            valor_saque = int(input('Digite o valor que deseja sacar: '))
            if valor_saque <= 0 :
                print('Não foi possível realizar o saque. Valor inválido')
            elif valor_saque > saldo:
                print('Não foi possível realizar o saque. Saldo insuficiente')
            elif valor_saque > 500:
                print('Não foi possível realizar o saque. Valor da operação maior que o permitido!')
            else:
                saldo -= valor_saque
                numero_saques +=1
                print('Saque realizado com sucesso!')
                extrato += f"Saque R${valor_saque:.2f} \n"
        else:
            print('Limite máximo de saques diários atingido!')
    
    elif opcao_usuario == 'e':
        print("######## EXTRATO ########")
        print(extrato)
        print(f'Saldo: R${saldo:.2f}')
        print("#########################")
    
    elif opcao_usuario == 'q':
        break

    else:
        print('Opção inválida! Por favor, digite novamente a opção desejada.')