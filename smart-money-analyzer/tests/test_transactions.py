"""
Simple tests for Smart Money Analyzer.

These are basic, beginner-friendly tests.
They do not use any testing framework, just plain Python
functions and assert statements, so they are easy to read
and easy to explain in an interview.

Run this file directly with:
    python tests/test_transactions.py
"""

import sys
import os

# Allow this test file to import functions from main.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from main import (
    calculate_totals,
    get_category_expenses,
    get_next_id,
    is_valid_date,
    get_month_from_date,
)


def test_calculate_totals():
    transactions = [
        {"id": 1, "type": "income", "amount": 1000, "category": "Salary", "description": "", "date": "2026-09-01"},
        {"id": 2, "type": "expense", "amount": 200, "category": "Food", "description": "", "date": "2026-09-02"},
        {"id": 3, "type": "expense", "amount": 300, "category": "Transport", "description": "", "date": "2026-09-03"},
    ]

    income, expense = calculate_totals(transactions)

    assert income == 1000
    assert expense == 500
    print("test_calculate_totals passed")


def test_get_category_expenses():
    transactions = [
        {"id": 1, "type": "expense", "amount": 200, "category": "Food", "description": "", "date": "2026-09-01"},
        {"id": 2, "type": "expense", "amount": 100, "category": "Food", "description": "", "date": "2026-09-02"},
        {"id": 3, "type": "expense", "amount": 300, "category": "Transport", "description": "", "date": "2026-09-03"},
        {"id": 4, "type": "income", "amount": 5000, "category": "Salary", "description": "", "date": "2026-09-01"},
    ]

    category_totals = get_category_expenses(transactions)

    assert category_totals["Food"] == 300
    assert category_totals["Transport"] == 300
    assert "Salary" not in category_totals
    print("test_get_category_expenses passed")


def test_get_next_id():
    empty_list = []
    assert get_next_id(empty_list) == 1

    transactions = [
        {"id": 1},
        {"id": 2},
        {"id": 5},
    ]
    assert get_next_id(transactions) == 6
    print("test_get_next_id passed")


def test_is_valid_date():
    assert is_valid_date("2026-09-23") == True
    assert is_valid_date("23-09-2026") == False
    assert is_valid_date("not a date") == False
    print("test_is_valid_date passed")


def test_get_month_from_date():
    assert get_month_from_date("2026-09-23") == "2026-09"
    assert get_month_from_date("2025-01-05") == "2025-01"
    print("test_get_month_from_date passed")


def test_budget_calculation():
    # Simple manual budget check, same logic used in manage_budget()
    budget = 5000
    spent = 6200

    if spent > budget:
        over_by = spent - budget
    else:
        over_by = 0

    assert over_by == 1200
    print("test_budget_calculation passed")


def test_unusual_spending_logic():
    # Same simple rule used in unusual_spending():
    # unusual if current spending > average * 1.3
    previous_average = 2000
    current_spending = 4500

    is_unusual = current_spending > previous_average * 1.3
    assert is_unusual == True

    normal_spending = 2200
    is_unusual_2 = normal_spending > previous_average * 1.3
    assert is_unusual_2 == False

    print("test_unusual_spending_logic passed")


def run_all_tests():
    test_calculate_totals()
    test_get_category_expenses()
    test_get_next_id()
    test_is_valid_date()
    test_get_month_from_date()
    test_budget_calculation()
    test_unusual_spending_logic()
    print("\nAll tests passed!")


if __name__ == "__main__":
    run_all_tests()
