print("================================")
print("       SMART MONEY ANALYZER")
print("================================")

while True:

    print("1. Add transaction")
    print("2. View transactions")
    print("3. Delete transaction")
    print("4. Search and filter")
    print("5. View summary")
    print("6. Manage budget")
    print("7. Monthly report")
    print("8. Spending analysis")
    print("9. Exit")

    choice = input("Enter ur choice: ")

    print("You entered:", choice)

    if choice == "9":
        print("Goodbye!")
        break