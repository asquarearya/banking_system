import os
import hashlib
from datetime import datetime
from random import randint

# Hashing the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generate a unique 6-digit account number
def generate_account_number():
    return str(randint(100000, 999999))

# Read all accounts from file
def read_accounts():
    if not os.path.exists("accounts.txt"):
        return []
    with open("accounts.txt", "r") as f:
        return [line.strip().split(',') for line in f.readlines()]

# Update account balance in file
def update_account_balance(account_number, new_balance):
    accounts = read_accounts()
    with open("accounts.txt", "w") as f:
        for acc in accounts:
            if acc[0] == account_number:
                acc[3] = str(new_balance)
            f.write(','.join(acc) + '\n')

# Log transaction in transactions.txt
def log_transaction(account_number, transaction_type, amount):
    with open("transactions.txt", "a") as f:
        f.write(f"{account_number},{transaction_type},{amount},{datetime.now().date()}\n")

# Create new account
def create_account():
    name = input("Enter your name: ")
    try:
        deposit = float(input("Enter your initial deposit: "))
    except ValueError:
        print("Invalid amount! Account not created.\n")
        return
    password = input("Enter your password: ")
    hashed_pwd = hash_password(password)
    account_number = generate_account_number()

    with open("accounts.txt", "a") as f:
        f.write(f"{account_number},{name},{hashed_pwd},{deposit}\n")

    print(f"\nYour account number is: {account_number}")
    print("Account created successfully!\n")

# Login to account
def login():
    acc_num = input("Enter your account number: ")
    password = hash_password(input("Enter your password: "))
    accounts = read_accounts()

    for acc in accounts:
        if acc[0] == acc_num and acc[2] == password:
            print("\nLogin successful!\n")
            banking_menu(acc_num)
            return
    print("Invalid account number or password.\n")

# Banking operations menu
def banking_menu(account_number):
    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Logout")
        choice = input("Enter your choice: ")

        accounts = read_accounts()
        balance = 0
        for acc in accounts:
            if acc[0] == account_number:
                balance = float(acc[3])
                break

        if choice == '1':
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                balance += amount
                update_account_balance(account_number, balance)
                log_transaction(account_number, 'Deposit', amount)
                print(f"Deposit successful! Current balance: {balance}")
            except ValueError:
                print("Invalid amount.")

        elif choice == '2':
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                if amount > balance:
                    print("Insufficient funds!")
                else:
                    balance -= amount
                    update_account_balance(account_number, balance)
                    log_transaction(account_number, 'Withdrawal', amount)
                    print(f"Withdrawal successful! Current balance: {balance}")
            except ValueError:
                print("Invalid amount.")

        elif choice == '3':
            print(f"Your current balance is: {balance}")

        elif choice == '4':
            print("Logged out.\n")
            break

        else:
            print("Invalid choice. Try again.")

# Main menu
def main():
    while True:
        print("Welcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.\n")

if __name__ == "__main__":
    main()
