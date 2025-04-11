import csv
import os
from datetime import datetime
from collections import defaultdict

FILENAME = 'expenses.csv'


def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_expense():
    print("\nAdd New Expense")
    date = input("Date (YYYY-MM-DD): ")
    if not is_valid_date(date):
        print(" Invalid date format. Please use YYYY-MM-DD.")
        return
    category = input("Category (e.g., Food, Transport): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Please enter a valid number for amount.")
        return
    description = input("Description: ")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("✅ Expense added successfully!")


def view_expenses():
    print("\n--- All Expenses ---")
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        count = 0
        for row in reader:
            print(f"{row[0]} | {row[1]:<10} | ₹{row[2]:<7} | {row[3]}")
            count += 1
        if count == 0:
            print("No expenses found.")


def search_expenses():
    print("\nSearch Expenses")
    choice = input("Search by (1) Date or (2) Category? ")
    keyword = input("Enter your search term: ").lower()
    index = 0 if choice == '1' else 1

    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        found = False
        for row in reader:
            if keyword in row[index].lower():
                print(f"{row[0]} | {row[1]:<10} | ₹{row[2]} | {row[3]}")
                found = True
        if not found:
            print(" No matching records found.")


def total_expenses():
    total = 0.0
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                total += float(row[2])
            except ValueError:
                continue
    print(f"\n💰 Total Expenses: ₹{total:.2f}")


def monthly_summary():
    summary = defaultdict(float)
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                month = row[0][:7]  # YYYY-MM
                summary[month] += float(row[2])
            except (IndexError, ValueError):
                continue

    print("Monthly Summary:")
    for month, total in sorted(summary.items()):
        print(f"{month}: ₹{total:.2f}")


def category_summary():
    summary = defaultdict(float)
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                summary[row[1].lower()] += float(row[2])
            except (IndexError, ValueError):
                continue

    print("\n📊 Category-wise Summary:")
    for category, total in sorted(summary.items()):
        print(f"{category.capitalize()}: ₹{total:.2f}")


def delete_expense():
    view_expenses()
    target_date = input("\nEnter date of expense to delete (YYYY-MM-DD): ")
    target_desc = input("Enter description of expense to delete: ")

    updated_rows = []
    deleted = False

    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == target_date and row[3].lower() == target_desc.lower():
                deleted = True
                continue
            updated_rows.append(row)

    if deleted:
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(updated_rows)
        print("Expense deleted.")
    else:
        print(" No matching expense found to delete.")


def main_menu():
    initialize_file()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Total Expenses")
        print("5. Monthly Summary")
        print("6. Category-wise Summary")
        print("7. Delete an Expense")
        print("8. Exit")

        choice = input("Choose an option (1–8): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            search_expenses()
        elif choice == '4':
            total_expenses()
        elif choice == '5':
            monthly_summary()
        elif choice == '6':
            category_summary()
        elif choice == '7':
            delete_expense()
        elif choice == '8':
            print("👋 Exiting... See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
