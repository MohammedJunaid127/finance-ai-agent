import sqlite3

conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER,
    category TEXT,
    description TEXT
)
""")

conn.commit()


def add_expense_db(amount, category, description):
    cursor.execute(
        "INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)",
        (amount, category, description)
    )
    conn.commit()


def get_expenses_db():
    cursor.execute("SELECT amount, category, description FROM expenses")
    return cursor.fetchall()