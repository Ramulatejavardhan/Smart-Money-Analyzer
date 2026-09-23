# Smart Money Analyzer

## 1. Project Name
Smart Money Analyzer

## 2. Project Description
Smart Money Analyzer is a terminal-based personal finance application built with core Python.
It lets a user record their income and expenses and then understand their spending habits
through simple, rule-based analysis — not just a list of transactions.

## 3. Problem It Solves
Most beginner expense trackers only let you add and view transactions. They don't help you
actually understand your money. Smart Money Analyzer answers questions such as:

- Where is my money going?
- Which category do I spend the most on?
- How much income and expense do I have?
- Did I stay within my budget?
- How much did I spend this month?
- Is my recent spending unusually high compared to before?
- Which category needs more attention?

## 4. Features
- Add income and expense transactions with validation
- View all transactions in a clean, readable format
- Delete a transaction by ID (with confirmation)
- Search and filter transactions by category, type, date, or description
- Financial summary (total income, total expense, balance)
- Budget system — set a budget per category and check if you exceeded it
- Monthly report — income, expense, balance, and top categories for a chosen month
- Spending analysis — category-wise spending with percentage breakdown
- Unusual spending detection — compares current month's spending per category
  against your previous average to flag categories where you're spending more than usual
- Simple, beginner-friendly error handling so invalid input never crashes the program

## 5. Technologies Used
- Python 3 (standard library only)
- `json` module for reading/writing data
- `os` module for file paths
- `datetime` module for date validation and month calculations
- JSON files for data storage (no database used)

No external packages, frameworks, or APIs are used.

## 6. Project Structure
```
smart-money-analyzer/
│
├── main.py                     # The entire application (menu + all features)
│
├── data/
│   ├── transactions.json       # Stores all transactions
│   └── budgets.json            # Stores category budgets
│
├── tests/
│   └── test_transactions.py    # Simple tests for core functions
│
├── README.md
└── .gitignore
```

## 7. What Each File Does
- **main.py** — Contains the main menu loop and every feature function
  (add, view, delete, search, summary, budget, monthly report, spending analysis,
  unusual spending detection).
- **data/transactions.json** — A JSON list where every transaction (income or expense)
  is stored as a dictionary with `id`, `type`, `amount`, `category`, `description`, `date`.
- **data/budgets.json** — A JSON dictionary mapping category name to its budget amount.
- **tests/test_transactions.py** — Plain Python functions with `assert` statements that
  test the core calculation logic (totals, category grouping, budget check, unusual
  spending rule, date handling).

## 8. How to Run
Make sure Python 3 is installed. From the `smart-money-analyzer` folder, run:

```bash
python main.py
```

Then choose an option from the menu using the number keys.

## 9. Example Usage
```
===== SMART MONEY ANALYZER =====
1. Add Transaction
2. View Transactions
3. Delete Transaction
4. Search & Filter
5. Financial Summary
6. Manage Budget
7. Monthly Report
8. Spending Analysis
9. Unusual Spending
0. Exit
Enter your choice: 1

===== ADD TRANSACTION =====
Enter type (income/expense): expense
Enter amount: ₹250
Enter category (e.g. Food, Rent, Salary): Food
Enter description: Lunch
Enter date (YYYY-MM-DD): 2026-09-23
Transaction added successfully with ID 1.
```

Sample spending analysis output:
```
===== SPENDING ANALYSIS =====
Food: ₹7500 -> 40.5%
Shopping: ₹5000 -> 27.0%
Transport: ₹3000 -> 16.2%

Highest Spending Category: Food
You are spending the most money on Food.
```

## 10. How to Test
Run the test file directly:

```bash
python tests/test_transactions.py
```

If everything works, you'll see each test print "passed" and a final
"All tests passed!" message.

## 11. Future Improvements
- Export reports to a text or CSV file
- Add multiple currency support
- Add yearly reports in addition to monthly reports
- Allow editing an existing transaction instead of only delete + re-add
- Add a simple savings goal tracker
