import json
import os
from datetime import datetime


# This is the main folder of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# File where all money records are saved
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "data", "transactions.json")
# File where all budget data is saved
BUDGETS_FILE = os.path.join(BASE_DIR, "data", "budgets.json")


def load_transactions():
    # Read the saved transactions from the file
    try:
        with open(TRANSACTIONS_FILE, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: transactions file was invalid. Starting fresh.")
        return []


def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(transactions, file, indent=4)


def load_budgets():
    try:
        with open(BUDGETS_FILE, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: budgets file was invalid. Starting fresh.")
        return {}


def save_budgets(budgets):
    with open(BUDGETS_FILE, "w") as file:
        json.dump(budgets, file, indent=4)


def get_next_id(transactions):
    if len(transactions) == 0:
        return 1
    all_ids = [t["id"] for t in transactions]
    return max(all_ids) + 1


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_valid_amount():
    # Keep asking until the user enters a correct positive number
    while True:
        amount_text = input("Enter amount: ₹").strip()
        try:
            amount = float(amount_text)
            if amount <= 0:
                print("Amount must be greater than 0. Try again.")
                continue
            return amount
        except ValueError:
            print("That is not a valid number. Try again.")


def get_valid_date():
    while True:
        date_text = input("Enter date (YYYY-MM-DD): ").strip()
        if is_valid_date(date_text):
            return date_text
        print("Invalid date format. Please use YYYY-MM-DD.")


def get_valid_type():
    while True:
        t_type = input("Enter type (income/expense): ").strip().lower()
        if t_type in ("income", "expense"):
            return t_type
        print("Type must be 'income' or 'expense'. Try again.")


def add_transaction():
    print("\n===== ADD TRANSACTION =====")

    # Load all old transactions first
    transactions = load_transactions()

    # Take all details from the user
    t_type = get_valid_type()
    amount = get_valid_amount()

    category = input("Enter category (e.g. Food, Rent, Salary): ").strip()
    while category == "":
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    description = input("Enter description: ").strip()
    date = get_valid_date()

    new_transaction = {
        "id": get_next_id(transactions),
        "type": t_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    # Add the new item to the list
    transactions.append(new_transaction)
    # Save the updated list back to the file
    save_transactions(transactions)

    print(f"Transaction added successfully with ID {new_transaction['id']}.")


def print_transaction(t):
    print("-" * 30)
    print(f"ID: {t['id']}")
    print(f"Type: {t['type']}")
    print(f"Amount: ₹{t['amount']}")
    print(f"Category: {t['category']}")
    print(f"Description: {t['description']}")
    print(f"Date: {t['date']}")


def view_transactions():
    print("\n===== ALL TRANSACTIONS =====")
    transactions = load_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for t in transactions:
        print_transaction(t)
    print("-" * 30)
    print(f"Total transactions: {len(transactions)}")


def delete_transaction():
    print("\n===== DELETE TRANSACTION =====")
    transactions = load_transactions()

    try:
        t_id = int(input("Enter transaction ID to delete: ").strip())
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    found = None
    for t in transactions:
        if t["id"] == t_id:
            found = t
            break

    if found is None:
        print("Transaction not found.")
        return

    print_transaction(found)
    confirm = input("Are you sure you want to delete this? (y/n): ").strip().lower()

    if confirm == "y":
        transactions.remove(found)
        save_transactions(transactions)
        print("Transaction deleted successfully.")
    else:
        print("Delete cancelled.")


def search_filter():
    print("\n===== SEARCH & FILTER =====")
    transactions = load_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    print("Search by:")
    print("1. Category")
    print("2. Type")
    print("3. Date")
    print("4. Description keyword")

    choice = input("Enter choice: ").strip()

    results = []

    if choice == "1":
        category = input("Enter category: ").strip().lower()
        for t in transactions:
            if t["category"].lower() == category:
                results.append(t)

    elif choice == "2":
        t_type = input("Enter type (income/expense): ").strip().lower()
        for t in transactions:
            if t["type"] == t_type:
                results.append(t)

    elif choice == "3":
        date = input("Enter date (YYYY-MM-DD): ").strip()
        for t in transactions:
            if t["date"] == date:
                results.append(t)

    elif choice == "4":
        keyword = input("Enter keyword: ").strip().lower()
        for t in transactions:
            if keyword in t["description"].lower():
                results.append(t)

    else:
        print("Invalid choice.")
        return

    if len(results) == 0:
        print("No matching transactions found.")
    else:
        for t in results:
            print_transaction(t)
        print("-" * 30)
        print(f"Matches found: {len(results)}")


def calculate_totals(transactions):
    total_income = 0
    total_expense = 0

    for t in transactions:
        if t["type"] == "income":
            total_income += t["amount"]
        elif t["type"] == "expense":
            total_expense += t["amount"]

    return total_income, total_expense


def financial_summary():
    print("\n===== FINANCIAL SUMMARY =====")
    transactions = load_transactions()

    total_income, total_expense = calculate_totals(transactions)
    balance = total_income - total_expense

    print(f"Total Income: ₹{total_income}")
    print(f"Total Expenses: ₹{total_expense}")
    print(f"Balance: ₹{balance}")
    print(f"Transactions: {len(transactions)}")

def get_category_expenses(transactions):
    category_totals = {}

    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            if category in category_totals:
                category_totals[category] += t["amount"]
            else:
                category_totals[category] = t["amount"]

    return category_totals


def manage_budget():
    print("\n===== MANAGE BUDGET =====")
    print("1. Set/Update Budget")
    print("2. View Budget Status")

    choice = input("Enter choice: ").strip()
    budgets = load_budgets()

    if choice == "1":
        category = input("Enter category: ").strip()
        while category == "":
            print("Category cannot be empty.")
            category = input("Enter category: ").strip()

        amount = get_valid_amount()
        budgets[category] = amount
        save_budgets(budgets)
        print(f"Budget for {category} set to ₹{amount}.")

    elif choice == "2":
        if len(budgets) == 0:
            print("No budgets set yet.")
            return

        transactions = load_transactions()
        category_expenses = get_category_expenses(transactions)

        print("\n----- BUDGET STATUS -----")
        for category, budget_amount in budgets.items():
            spent = category_expenses.get(category, 0)
            print(f"\n{category} Budget: ₹{budget_amount}")
            print(f"{category} Spending: ₹{spent}")

            if spent > budget_amount:
                over = spent - budget_amount
                print(f"Status: Budget exceeded by ₹{over}")
            else:
                remaining = budget_amount - spent
                print(f"Status: Within budget. ₹{remaining} remaining")

    else:
        print("Invalid choice.")


def get_month_from_date(date_text):
    return date_text[:7]


def monthly_report():
    print("\n===== MONTHLY REPORT =====")
    month = input("Enter month (YYYY-MM): ").strip()

    transactions = load_transactions()
    month_transactions = [t for t in transactions if get_month_from_date(t["date"]) == month]

    if len(month_transactions) == 0:
        print("No transactions found for this month.")
        return

    total_income, total_expense = calculate_totals(month_transactions)
    balance = total_income - total_expense
    category_expenses = get_category_expenses(month_transactions)

    print(f"\n===== REPORT FOR {month} =====")
    print(f"Income: ₹{total_income}")
    print(f"Expenses: ₹{total_expense}")
    print(f"Balance: ₹{balance}")

    if len(category_expenses) > 0:
        print("\nTop spending categories:")
        sorted_categories = sorted(category_expenses.items(), key=lambda item: item[1], reverse=True)
        for category, amount in sorted_categories:
            print(f"{category}: ₹{amount}")


def spending_analysis():
    print("\n===== SPENDING ANALYSIS =====")
    transactions = load_transactions()

    category_expenses = get_category_expenses(transactions)

    if len(category_expenses) == 0:
        print("No expenses recorded yet.")
        return

    total_spending = sum(category_expenses.values())

    sorted_categories = sorted(category_expenses.items(), key=lambda item: item[1], reverse=True)

    for category, amount in sorted_categories:
        percentage = (amount / total_spending) * 100
        print(f"{category}: ₹{amount} -> {percentage:.1f}%")

    highest_category = sorted_categories[0][0]
    print(f"\nHighest Spending Category: {highest_category}")
    print(f"You are spending the most money on {highest_category}.")


def get_latest_month(transactions):
    months = [get_month_from_date(t["date"]) for t in transactions]
    if len(months) == 0:
        return None
    return max(months)


def unusual_spending():
    print("\n===== UNUSUAL SPENDING =====")
    transactions = load_transactions()
    expense_transactions = [t for t in transactions if t["type"] == "expense"]

    if len(expense_transactions) == 0:
        print("No expenses recorded yet.")
        return

    latest_month = get_latest_month(expense_transactions)

    current_month_expenses = {}
    previous_months_expenses = {}

    for t in expense_transactions:
        month = get_month_from_date(t["date"])
        category = t["category"]

        if month == latest_month:
            current_month_expenses[category] = current_month_expenses.get(category, 0) + t["amount"]
        else:
            if category not in previous_months_expenses:
                previous_months_expenses[category] = {}
            previous_months_expenses[category][month] = previous_months_expenses[category].get(month, 0) + t["amount"]

    found_unusual = False

    for category, current_amount in current_month_expenses.items():
        if category in previous_months_expenses:
            monthly_totals = list(previous_months_expenses[category].values())
            average = sum(monthly_totals) / len(monthly_totals)

            if average > 0 and current_amount > average * 1.3:
                found_unusual = True
                print(f"\n{category} spending is higher than your usual spending.")
                print(f"Previous average: ₹{average:.0f}")
                print(f"Current spending: ₹{current_amount}")

    if not found_unusual:
        print("No unusual spending detected. Your spending looks normal.")


def show_menu():
    print("===== SMART MONEY ANALYZER =====")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Delete Transaction")
    print("4. Search & Filter")
    print("5. Financial Summary")
    print("6. Manage Budget")
    print("7. Monthly Report")
    print("8. Spending Analysis")
    print("9. Unusual Spending")
    print("10. Exit")

def main():
    # its Keep the app running until the user chooses Exit
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            delete_transaction()
        elif choice == "4":
            search_filter()
        elif choice == "5":
            financial_summary()
        elif choice == "6":
            manage_budget()
        elif choice == "7":
            monthly_report()
        elif choice == "8":
            spending_analysis()
        elif choice == "9":
            unusual_spending()
        elif choice == "10":
            print("Thank you for using Smart Money Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1-10.")
if __name__ == "__main__":
    main()
