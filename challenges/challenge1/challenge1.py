import os

menu = """
    Escolha a operação que deseja realizar

    [d] Depósito
    [s] Saque
    [e] Extrato

    [q] Sair
"""

balance = 0.0
extrato = ""

number_of_withdrawals = 0
WITHDRAWAL_LIMIT = 3

def clear_console():
    os.system("cls")

def deposit(value):

    global balance, extrato

    if value > 0.0:
        balance += value
        extrato += f"Depósito R$ {value:.2f}\n"
        print("Depósito concluído com sucesso!")
    else:
        print("Operação abortada! O valor do depósito é inválido.")

    input("Digite qualquer tecla para continuar...")

    return

def withdrawal(value):

    global balance, extrato, number_of_withdrawals

    if number_of_withdrawals >= WITHDRAWAL_LIMIT:
        print("Limite de saques diário atingido! Volte amanhã.")
        return

    if value > 0.0 and balance >= value:
        balance -= value
        extrato += f"Saque R$ {value:.2f}\n"
        number_of_withdrawals += 1
        print("Saque concluído com sucesso!")
    else:
        if value > 0.0:
            print("Saldo insuficiente para a operação.")
        else:
            print("Operação abortada! O valor do saque é inválido.")
    
    input("Digite qualquer tecla para continuar...")

    return

def show_statement():

    global extrato

    clear_console()

    print("\n========== EXTRATO ==========")
    print("Nenhuma operação realizada!" if not extrato else extrato)
    print(f"Saldo: R$ {balance:.2f}")
    print("=============================\n")

    input("Digite qualquer tecla para continuar...")

def main():

    while True:

        option = input(menu)

        if option == "d":
            try:
                value = float(input("Quanto deseja depositar? "))
                deposit(value)
            except ValueError:
                print("Insira um valor numérico válido!")
        elif option == "s":
            try:
                value = float(input("Quanto deseja sacar? "))
                withdrawal(value)
            except ValueError:
                print("Insira um valor numérico válido!")
        elif option == "e":
            show_statement()
        elif option == "q":
            print("Saindo...")
            break
        else:
            print("Operação inválida!")

if __name__ == "__main__":
    main()
