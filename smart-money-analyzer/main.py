import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "transactions.json"


def load_transactions():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            transactions = json.load(file)
        if not isinstance(transactions, list):
            return []
        return transactions
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_transactions(transactions):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)


def get_next_id(transactions):
    if not transactions:
        return 1

    largest_id = 0
    for transaction in transactions:
        if transaction["id"] > largest_id:
            largest_id = transaction["id"]
    return largest_id + 1


def add_transaction():
    transactions = load_transactions()

    transaction_type = input("Type (income/expense): ").strip().lower()
    if transaction_type not in ("income", "expense"):
        print("Invalid transaction type.")
        return

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    category = input("Category: ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    transaction_date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    transaction = {
        "id": get_next_id(transactions),
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": transaction_date,
    }
    transactions.append(transaction)
    save_transactions(transactions)
    print("Transaction saved successfully.")


def view_transactions():
    transactions = load_transactions()
    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(
            f"ID: {transaction['id']} | "
            f"Type: {transaction['type']} | "
            f"Amount: {transaction['amount']:.2f} | "
            f"Category: {transaction['category']} | "
            f"Description: {transaction['description']} | "
            f"Date: {transaction['date']}"
        )


def main():
    while True:
        print("\n=== SMART MONEY ANALYZER ===")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Delete transaction")
        print("4. Search and filter")
        print("5. View summary")
        print("6. Manage budget")
        print("7. Monthly report")
        print("8. Spending analysis")
        print("9. Unusual spending")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "0":
            print("Goodbye!")
            break
        elif choice in ("3", "4", "5", "6", "7", "8", "9"):
            print("This feature will be added in a later stage.")
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()