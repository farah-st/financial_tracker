import sqlite3
import plotly.express as px
import pandas as pd

def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        category TEXT,
                        amount REAL,
                        date TEXT)''')
    conn.commit()
    conn.close()

def add_transaction(t_type, category, amount, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                   (t_type, category, amount, date))
    conn.commit()
    conn.close()

def view_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_expense_bar_chart():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM transactions WHERE type='Expense' GROUP BY category", conn)
    conn.close()
    if df.empty:
        print("No expense data available for visualization.")
        return
    fig = px.bar(df, x='category', y='total', title='Spending by Category', labels={'total': 'Amount Spent'})
    fig.show()

def generate_pie_chart():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM transactions WHERE type='Expense' GROUP BY category", conn)
    conn.close()
    if df.empty:
        print("No expense data available for visualization.")
        return
    fig = px.pie(df, names='category', values='total', title='Expense Distribution')
    fig.show()

def search_transactions_by_category():
    category = input("Enter category to search: ")
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE category=?", (category,))
    results = cursor.fetchall()
    conn.close()
    if not results:
        print("No transactions found in this category.")
    else:
        for row in results:
            print(row)

def delete_transaction_by_id():
    t_id = int(input("Enter transaction ID to delete: "))
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (t_id,))
    conn.commit()
    conn.close()
    print(f"Transaction with ID {t_id} deleted.")

def edit_transaction():
    t_id = int(input("Enter transaction ID to edit: "))
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id=?", (t_id,))
    row = cursor.fetchone()
    if row:
        print(f"Current details: {row}")
        new_type = input("Enter new type (Income/Expense): ").capitalize()
        new_category = input("Enter new category: ")
        new_amount = float(input("Enter new amount: "))
        new_date = input("Enter new date (YYYY-MM-DD): ")
        cursor.execute("UPDATE transactions SET type=?, category=?, amount=?, date=? WHERE id=?",
                       (new_type, new_category, new_amount, new_date, t_id))
        conn.commit()
        print("Transaction updated successfully.")
    else:
        print("Transaction ID not found.")
    conn.close()

def list_transaction_summary():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type, COUNT(*) as count, SUM(amount) as total FROM transactions GROUP BY type")
    results = cursor.fetchall()
    conn.close()
    if results:
        for result in results:
            print(f"Type: {result[0]}, Count: {result[1]}, Total: {result[2]}")
    else:
        print("No transactions found.")

def menu():
    init_db()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Visualize Spending (Bar Chart)")
        print("4. Visualize Spending (Pie Chart)")
        print("5. Search Transactions by Category")
        print("6. Delete Transaction")
        print("7. Edit Transaction")
        print("8. List Transaction Summary")
        print("9. Exit")
        choice = input("Please select an option: ")
        if choice == "1":
            t_type = input("Enter transaction type (Income/Expense): ").capitalize()
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            date = input("Enter date (YYYY-MM-DD): ")
            add_transaction(t_type, category, amount, date)
            print("Transaction added successfully!")
        elif choice == "2":
            transactions = view_transactions()
            print("\nTransactions:")
            for t in transactions:
                print(t)
        elif choice == "3":
            generate_expense_bar_chart()
        elif choice == "4":
            generate_pie_chart()
        elif choice == "5":
            search_transactions_by_category()
        elif choice == "6":
            delete_transaction_by_id()
        elif choice == "7":
            edit_transaction()
        elif choice == "8":
            list_transaction_summary()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    menu()

#.\venv\Scripts\activate
#python src/main.py
#source venv/bin/activate