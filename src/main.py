import sqlite3
import plotly.express as px
import pandas as pd

# Database setup
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

# Function to add transactions
def add_transaction(t_type, category, amount, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                   (t_type, category, amount, date))
    conn.commit()
    conn.close()

# Function to view all transactions
def view_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to generate bar chart
def visualize_spending():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM transactions WHERE type='Expense' GROUP BY category", conn)
    conn.close()
    
    if df.empty:
        print("No expense data available for visualization.")
        return
    
    fig = px.bar(df, x='category', y='total', title='Spending by Category', labels={'total': 'Amount Spent'})
    fig.show()

# Function to generate pie chart
def spending_pie_chart():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM transactions WHERE type='Expense' GROUP BY category", conn)
    conn.close()
    
    if df.empty:
        print("No expense data available for visualization.")
        return
    
    fig = px.pie(df, names='category', values='total', title='Expense Distribution')
    fig.show()

# CLI Menu
def main():
    init_db()
    choices = ["1", "2", "3", "4", "5"]
    predefined_inputs = iter(["1", "Expense", "Food", "20", "2025-03-02", "2", "5"])  # Replace with needed test cases
    
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Visualize Spending (Bar Chart)")
        print("4. Visualize Spending (Pie Chart)")
        print("5. Exit")
        
        try:
            choice = next(predefined_inputs)  # Simulating user input
            print(f"Selected: {choice}")
        except StopIteration:
            print("No more predefined inputs. Exiting...")
            break
        
        if choice == "1":
            try:
                t_type = next(predefined_inputs).capitalize()
                category = next(predefined_inputs)
                amount = float(next(predefined_inputs))
                date = next(predefined_inputs)
                add_transaction(t_type, category, amount, date)
                print("Transaction added successfully!")
            except StopIteration:
                print("Missing input values for transaction. Skipping...")
                
        elif choice == "2":
            transactions = view_transactions()
            print("\nTransactions:")
            for t in transactions:
                print(t)
            
        elif choice == "3":
            visualize_spending()
            
        elif choice == "4":
            spending_pie_chart()
            
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()

#.\venv\Scripts\activate
#source venv/bin/activate