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

    if choice == "1":
        print("Add transaction")

    elif choice == "2":
        print("View transactions")

    elif choice == "3":
        print("Delete transaction")

    elif choice == "4":
        print("Search and filter")

    elif choice == "5":
        print("View summary")

    elif choice == "6":
        print("Manage budget")

    elif choice == "7":
        print("Monthly report")

    elif choice == "8":
        print("Spending analysis")

    elif choice == "9":
        print("See u again, bye!")
        break

    else:
        print("Select a valid choice")