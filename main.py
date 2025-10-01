from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        # New table for income/credits
        c.execute("""
            CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def edit_expense(expense_id, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Edit an existing expense entry. Only provided fields will be updated.'''
    with sqlite3.connect(DB_PATH) as c:
        # First check if expense exists
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Expense with id {expense_id} not found"}
        
        # Build dynamic update query
        updates = []
        params = []
        
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if subcategory is not None:
            updates.append("subcategory = ?")
            params.append(subcategory)
        if note is not None:
            updates.append("note = ?")
            params.append(note)
        
        if not updates:
            return {"status": "error", "message": "No fields to update"}
        
        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, params)
        
        return {"status": "ok", "id": expense_id, "updated_fields": len(updates)}

@mcp.tool()
def delete_expense(expense_id):
    '''Delete an expense entry by ID.'''
    with sqlite3.connect(DB_PATH) as c:
        # Check if expense exists
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Expense with id {expense_id} not found"}
        
        c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return {"status": "ok", "id": expense_id, "message": "Expense deleted successfully"}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, id DESC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def add_income(date, amount, source, note=""):
    '''Add income/credit entry (e.g., salary, bonus, refund).'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO income(date, amount, source, note) VALUES (?,?,?,?)",
            (date, amount, source, note)
        )
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def list_income(start_date, end_date):
    '''List income entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, source, note
            FROM income
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, id DESC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def edit_income(income_id, date=None, amount=None, source=None, note=None):
    '''Edit an existing income entry. Only provided fields will be updated.'''
    with sqlite3.connect(DB_PATH) as c:
        # Check if income exists
        cur = c.execute("SELECT * FROM income WHERE id = ?", (income_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Income with id {income_id} not found"}
        
        # Build dynamic update query
        updates = []
        params = []
        
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if source is not None:
            updates.append("source = ?")
            params.append(source)
        if note is not None:
            updates.append("note = ?")
            params.append(note)
        
        if not updates:
            return {"status": "error", "message": "No fields to update"}
        
        params.append(income_id)
        query = f"UPDATE income SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, params)
        
        return {"status": "ok", "id": income_id, "updated_fields": len(updates)}

@mcp.tool()
def delete_income(income_id):
    '''Delete an income entry by ID.'''
    with sqlite3.connect(DB_PATH) as c:
        # Check if income exists
        cur = c.execute("SELECT * FROM income WHERE id = ?", (income_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Income with id {income_id} not found"}
        
        c.execute("DELETE FROM income WHERE id = ?", (income_id,))
        return {"status": "ok", "id": income_id, "message": "Income deleted successfully"}

@mcp.tool()
def get_balance(start_date, end_date):
    '''Calculate net balance (total income - total expenses) for a date range.'''
    with sqlite3.connect(DB_PATH) as c:
        # Get total expenses
        cur = c.execute(
            "SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        total_expenses = cur.fetchone()[0] or 0
        
        # Get total income
        cur = c.execute(
            "SELECT SUM(amount) FROM income WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        total_income = cur.fetchone()[0] or 0
        
        balance = total_income - total_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "start_date": start_date,
            "end_date": end_date
        }

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY total_amount DESC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()