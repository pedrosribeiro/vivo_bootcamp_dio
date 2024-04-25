import os


def clear_console():
    os.system("cls")


# positional only arguments
def deposit(balance, value, statement, /):

    if value > 0.0:
        balance += value
        statement += f"Depósito R$ {value:.2f}\n"
        print("Depósito concluído com sucesso!")
    else:
        print("Operação abortada! O valor do depósito é inválido.")

    input("Digite qualquer tecla para continuar...")

    return balance, statement


# keyword only arguments
def withdrawal(*, balance, value, statement, number_of_withdrawals, withdrawal_limit):

    if number_of_withdrawals >= withdrawal_limit:
        print("Limite de saques diário atingido! Volte amanhã.")
        return

    if value > 0.0 and balance >= value:
        balance -= value
        statement += f"Saque R$ {value:.2f}\n"
        number_of_withdrawals += 1
        print("Saque concluído com sucesso!")
    else:
        if value > 0.0:
            print("Saldo insuficiente para a operação.")
        else:
            print("Operação abortada! O valor do saque é inválido.")

    input("Digite qualquer tecla para continuar...")

    return balance, statement


# positional and keyword arguments
def show_statement(balance, /, *, statement):

    clear_console()

    print("\n========== EXTRATO ==========")
    print("Nenhuma operação realizada!" if not statement else statement)
    print(f"Saldo: R$ {balance:.2f}")
    print("=============================\n")

    input("Digite qualquer tecla para continuar...")


def create_user(users):

    cpf = input("Informe o CPF do novo usuário (apenas números)")
    user = get_user_by_cpf(users, cpf)

    if user:
        print("Usuário já cadastrado!")
        return

    name = input("Informe o nome: ")
    birth_date = input("Informe a data de nascimento (dd/mm/aa): ")
    address = input("Informe o endereço (rua, número - bairro - cidade/UF): ")

    user = {"name": name, "birth_date": birth_date, "cpf": cpf, "address": address}

    users.append(user)

    print("Usuário cadastrado com sucesso!")

    return users


def get_user_by_cpf(users, cpf):

    user = [user for user in users if user["cpf"] == cpf]

    return user[0] if user else None


def create_checking_account(branch, checking_accounts: list, users):

    cpf = input("Informe o CPF do usuário (apenas números)")
    user = get_user_by_cpf(users, cpf)

    if user:
        account_number = len(checking_accounts) + 1
        account = {"branch": branch, "account_number": account_number, "user": user}

        print("Conta criada com sucesso!")

        return account

    print("A conta não foi criada: usuário não encontrado!")

    return None


def list_accounts(accounts):
    for acc in accounts:
        result = f"""
            =======================
            Agência: {acc["branch"]}
            Número da conta: {acc["account_number"]}
            Titular: {acc["user"]["name"]}
            =======================
        """
        print(result)


def menu():
    menu = """
        Escolha a operação que deseja realizar

        [d] Depósito
        [s] Saque
        [e] Extrato
        [nu] Novo usuário
        [nc] Nova conta
        [lc] Listar contas

        [q] Sair
    """

    return input(menu)


def main():

    WITHDRAWAL_LIMIT = 3
    BRANCH = "0001"

    balance = 0.0
    statement = ""
    number_of_withdrawals = 0
    users = []
    checking_accounts = []

    while True:

        option = menu()

        if option == "d":
            try:
                value = float(input("Quanto deseja depositar? "))
                balance, statement = deposit(balance, value, statement)
            except ValueError:
                print("Insira um valor numérico válido!")
        elif option == "s":
            try:
                value = float(input("Quanto deseja sacar? "))
                balance, statement = withdrawal(
                    balance=balance,
                    value=value,
                    statement=statement,
                    number_of_withdrawals=number_of_withdrawals,
                    withdrawal_limit=WITHDRAWAL_LIMIT,
                )
            except ValueError:
                print("Insira um valor numérico válido!")
        elif option == "e":
            show_statement(balance, statement=statement)
        elif option == "nu":
            create_user(users)
        elif option == "nc":

            account = create_checking_account(BRANCH, checking_accounts, users)

            if account:
                checking_accounts.append(account)

        elif option == "lc":
            list_accounts(checking_accounts)
        elif option == "q":
            print("Saindo...")
            break
        else:
            print("Operação inválida!")


if __name__ == "__main__":
    main()
