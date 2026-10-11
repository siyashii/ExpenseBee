import sqlite3


from datetime import date

expenses = []

def init_db():
    conn = sqlite3.connect("expensebee.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount in rupees: "))

            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def add_expense():
    amount = get_valid_amount()
    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        print("Expense was not added.")
        return

    expense_date = date.today().isoformat()

    conn = sqlite3.connect("expensebee.db")

    conn.execute(
        """
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
        """,
        (amount, category, description, expense_date)
    )

    conn.commit()
    conn.close()

    print("Expense added successfully!")


    
    
def view_expenses():
    conn = sqlite3.connect("expensebee.db")

    cursor = conn.execute(
        """
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY id
        """
    )

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0

    print("\nYour expenses:")

    for number, expense in enumerate(expenses, start=1):
        expense_id, amount, category, description, expense_date = expense

        print(
            f"{number}. {category} - {description} - "
            f"Rs. {amount:.2f} - {expense_date}"
        )

        total += amount

    print(f"\nTotal spending: Rs. {total:.2f}")  
    

def delete_expense():
    conn = sqlite3.connect("expensebee.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
    """)

    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found to delete.")
        conn.close()
        return

    print("\n--- Your Expenses ---")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )

    try:
        expense_id = int(input("\nEnter the ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        conn.close()
        return

    cursor.execute(
        "SELECT id FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:
        print("Expense ID not found.")
        conn.close()
        return

    confirm = input(
        "Are you sure you want to delete this expense? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        conn.commit()
        print("Expense deleted successfully!")
    else:
        print("Deletion cancelled.")

    conn.close()   
    

def update_expense():
    conn = sqlite3.connect("expensebee.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
    """)

    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found to update.")
        conn.close()
        return

    print("\n--- Your Expenses ---")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )

    try:
        expense_id = int(input("\nEnter the ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        conn.close()
        return

    cursor.execute(
        "SELECT id FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:
        print("Expense ID not found.")
        conn.close()
        return

    try:
        new_amount = float(input("Enter the new amount: "))

        if new_amount <= 0:
            print("Amount must be greater than zero.")
            conn.close()
            return

    except ValueError:
        print("Invalid amount. Please enter a number.")
        conn.close()
        return

    confirm = input(
        f"Update expense ID {expense_id} to ₹{new_amount:.2f}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
            """,
            (new_amount, expense_id)
        )

        conn.commit()
        print("Expense updated successfully!")
    else:
        print("Update cancelled.")

    conn.close()


def monthly_summary():
    conn = sqlite3.connect("expensebee.db")
    cursor = conn.cursor()

    month = input("Enter the month (YYYY-MM): ").strip()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date LIKE ?",
        (month + "%",)
    )

    total = cursor.fetchone()[0]

    if total is None:
        print("No expenses found for this month.")
    else:
        print(f"Total spending for {month}: ₹{total:.2f}")

    conn.close()
    

def category_summary():
    conn = sqlite3.connect("expensebee.db")
    cursor = conn.cursor()
    
    category = input("Enter the category you want to summarize: ").strip()
    
    cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE category =  ?",
            (category,)
    )
    
    total = cursor.fetchone()[0]
    
    if total is None:
            print("No expenses found for this category.")
    else:
            print(f"Total spending for {category}: ₹{total:.2f}")
    
    
    conn.close()
    
    

def main():
    init_db()

    while True:
        print("\n===== ExpenseBee =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Monthly Expense")
        print("6. Category-wise Summary")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            category_summary()
        elif choice == "7":
            print("Thank you for using ExpenseBee!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()