"""A small command-line personal finance tracker using only the standard library."""

from __future__ import annotations

import json
import uuid
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"
CATEGORIES = ("Food", "Transport", "Shopping", "Education", "Bills", "Entertainment", "Health", "Other")


def validate_date(value: str) -> str:
    """Return a valid YYYY-MM-DD date or raise ValueError."""
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as error:
        raise ValueError("Date must use YYYY-MM-DD format.") from error
    return parsed.isoformat()


def validate_amount(value: str | float | int) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Amount must be a number.") from error
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


class TransactionManager:
    def __init__(self, file_path: Path = TRANSACTIONS_FILE):
        self.file_path = Path(file_path)
        self.transactions = self._load()

    def _load(self) -> list[dict[str, Any]]:
        try:
            with self.file_path.open(encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError
        except (OSError, json.JSONDecodeError, ValueError):
            return []
        valid = []
        for transaction in data:
            if isinstance(transaction, dict) and {"id", "type", "amount", "category", "description", "date"} <= transaction.keys():
                valid.append(transaction)
        return valid

    def save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.transactions, file, indent=4)

    def add(self, transaction_type: str, amount: float | str, category: str, description: str, transaction_date: str) -> dict[str, Any]:
        if transaction_type not in ("income", "expense"):
            raise ValueError("Type must be income or expense.")
        if not category.strip():
            raise ValueError("Category is required.")
        transaction = {
            "id": uuid.uuid4().hex[:8],
            "type": transaction_type,
            "amount": validate_amount(amount),
            "category": category.strip().title(),
            "description": description.strip(),
            "date": validate_date(transaction_date),
        }
        self.transactions.append(transaction)
        self.save()
        return transaction

    def delete(self, transaction_id: str) -> bool:
        original_count = len(self.transactions)
        self.transactions = [item for item in self.transactions if item["id"] != transaction_id]
        if len(self.transactions) == original_count:
            return False
        self.save()
        return True

    def search(self, transaction_type: str | None = None, category: str | None = None, transaction_date: str | None = None, description: str | None = None) -> list[dict[str, Any]]:
        return [
            item for item in self.transactions
            if (not transaction_type or item["type"] == transaction_type)
            and (not category or item["category"].lower() == category.lower())
            and (not transaction_date or item["date"] == transaction_date)
            and (not description or description.lower() in item["description"].lower())
        ]

    def summary(self) -> dict[str, float | int]:
        incomes = [item["amount"] for item in self.transactions if item["type"] == "income"]
        expenses = [item["amount"] for item in self.transactions if item["type"] == "expense"]
        total_income, total_expenses = sum(incomes), sum(expenses)
        return {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "balance": round(total_income - total_expenses, 2),
            "transaction_count": len(self.transactions),
            "highest_expense": max(expenses, default=0),
            "average_expense": round(total_expenses / len(expenses), 2) if expenses else 0,
        }

    def monthly_report(self, month: str) -> dict[str, Any]:
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError as error:
            raise ValueError("Month must use YYYY-MM format.") from error
        transactions = [item for item in self.transactions if item["date"].startswith(month)]
        category_totals = defaultdict(float)
        income = sum(item["amount"] for item in transactions if item["type"] == "income")
        expenses = sum(item["amount"] for item in transactions if item["type"] == "expense")
        for item in transactions:
            if item["type"] == "expense":
                category_totals[item["category"]] += item["amount"]
        return {"income": income, "expenses": expenses, "balance": income - expenses, "category_spending": dict(category_totals)}

    def analysis(self) -> dict[str, Any]:
        expenses = [item for item in self.transactions if item["type"] == "expense"]
        category_spending = defaultdict(float)
        for item in expenses:
            category_spending[item["category"]] += item["amount"]
        summary = self.summary()
        income = summary["total_income"]
        return {
            "highest_category": max(category_spending, key=category_spending.get, default="None"),
            "category_spending": dict(category_spending),
            "largest_transaction": max(expenses, key=lambda item: item["amount"], default=None),
            "average_expense": summary["average_expense"],
            "savings": summary["balance"],
            "savings_rate": round(summary["balance"] / income * 100, 2) if income else 0,
        }

    def unusual_expenses(self) -> list[dict[str, str]]:
        expenses = [item for item in self.transactions if item["type"] == "expense"]
        if not expenses:
            return []
        average = sum(item["amount"] for item in expenses) / len(expenses)
        return [{"id": item["id"], "reason": f"Amount is at least twice the average expense ({average:.2f})."} for item in expenses if item["amount"] >= average * 2]


class BudgetManager:
    def __init__(self, file_path: Path = BUDGETS_FILE):
        self.file_path = Path(file_path)
        self.budgets = self._load()

    def _load(self) -> dict[str, float]:
        try:
            with self.file_path.open(encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def set(self, category: str, amount: float | str) -> None:
        self.budgets[category.title()] = validate_amount(amount)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.budgets, file, indent=4)

    def status(self, manager: TransactionManager) -> dict[str, dict[str, float | bool]]:
        spending = manager.analysis()["category_spending"]
        return {category: {"budget": budget, "spent": spending.get(category, 0), "remaining": round(budget - spending.get(category, 0), 2), "exceeded": spending.get(category, 0) > budget} for category, budget in self.budgets.items()}


def print_transactions(transactions: list[dict[str, Any]]) -> None:
    if not transactions:
        print("No transactions found.")
        return
    for item in transactions:
        print(f'{item["id"]} | {item["date"]} | {item["type"]:7} | {item["amount"]:10.2f} | {item["category"]} | {item["description"]}')


def prompt_add(manager: TransactionManager) -> None:
    try:
        transaction = manager.add(input("Type (income/expense): ").strip().lower(), input("Amount: "), input("Category: "), input("Description: "), input("Date (YYYY-MM-DD): "))
        print(f'Saved transaction {transaction["id"]}.')
    except ValueError as error:
        print(f"Error: {error}")


def run_cli() -> None:
    manager, budgets = TransactionManager(), BudgetManager()
    actions = {"1": lambda: prompt_add(manager), "2": lambda: print_transactions(manager.transactions), "3": lambda: print("Deleted." if manager.delete(input("Transaction ID: ").strip()) else "Transaction not found."), "4": lambda: print_transactions(manager.search(input("Type (blank for any): ").strip() or None, input("Category (blank for any): ").strip() or None, input("Date (blank for any): ").strip() or None, input("Description (blank for any): ").strip() or None)), "5": lambda: print(manager.summary()), "6": lambda: manage_budget(manager, budgets), "7": lambda: print(manager.monthly_report(input("Month (YYYY-MM): ").strip())), "8": lambda: print(manager.analysis()), "9": lambda: print_unusual(manager)}
    while True:
        print("\n=== SMART MONEY ANALYZER ===")
        print("1. Add transaction\n2. View transactions\n3. Delete transaction\n4. Search and filter\n5. Financial summary\n6. Manage budget\n7. Monthly report\n8. Spending analysis\n9. Unusual spending\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except ValueError as error:
                print(f"Error: {error}")
        else:
            print("Please choose a valid option.")


def manage_budget(manager: TransactionManager, budgets: BudgetManager) -> None:
    category = input(f"Category ({', '.join(CATEGORIES)}): ").strip().title()
    try:
        budgets.set(category, input("Budget amount: "))
        status = budgets.status(manager)[category]
        print(f"Budget saved. Remaining: {status['remaining']:.2f}")
        if status["exceeded"]:
            print("Warning: this budget has been exceeded.")
    except ValueError as error:
        print(f"Error: {error}")


def print_unusual(manager: TransactionManager) -> None:
    unusual = manager.unusual_expenses()
    if not unusual:
        print("No unusual expenses detected.")
    for item in unusual:
        print(f'{item["id"]}: {item["reason"]}')


if __name__ == "__main__":
    run_cli()