# 💰 Expense Tracker MCP Server

A Model Context Protocol (MCP) server for tracking personal expenses and income, built with FastMCP and SQLite.

## Features

- **Expense Management**: Add, edit, delete, and list expenses with categories and subcategories
- **Income Tracking**: Record salary, bonuses, refunds, and other income sources
- **Balance Calculation**: Get net balance (income - expenses) for any date range
- **Expense Summaries**: Analyze spending by category
- **Date Range Queries**: Filter transactions by date
- **Persistent Storage**: SQLite database for reliable data storage

## Installation

1. Clone this repository or download the files

2. Install dependencies:
```bash
pip install fastmcp
```

3. The server will automatically create the SQLite database on first run

## Usage

### Running the MCP Server

```bash
python main.py
```

Or using UV:
```bash
uv run fastmcp install main.py
```

### Configuring with Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ExpenseTracker": {
      "command": "python",
      "args": ["/path/to/your/main.py"]
    }
  }
}
```

Or using UV:
```json
{
  "mcpServers": {
    "ExpenseTracker": {
      "command": "uv",
      "args": ["run", "fastmcp", "run", "/path/to/your/main.py"]
    }
  }
}
```

## Available Tools

### Expense Operations

- **`add_expense(date, amount, category, subcategory="", note="")`**
  - Add a new expense entry
  - Example: `add_expense("2025-10-01", 50.00, "Food", "Lunch", "Pizza with friends")`

- **`edit_expense(expense_id, date=None, amount=None, category=None, subcategory=None, note=None)`**
  - Edit an existing expense (only updates provided fields)
  - Example: `edit_expense(1, amount=55.00, note="Updated amount")`

- **`delete_expense(expense_id)`**
  - Delete an expense by ID
  - Example: `delete_expense(1)`

- **`list_expenses(start_date, end_date)`**
  - List all expenses within a date range
  - Example: `list_expenses("2025-10-01", "2025-10-31")`

### Income Operations

- **`add_income(date, amount, source, note="")`**
  - Add income/credit entry
  - Example: `add_income("2025-10-01", 5000.00, "Salary", "October salary")`

- **`edit_income(income_id, date=None, amount=None, source=None, note=None)`**
  - Edit an existing income entry
  - Example: `edit_income(1, amount=5500.00)`

- **`delete_income(income_id)`**
  - Delete an income entry by ID
  - Example: `delete_income(1)`

- **`list_income(start_date, end_date)`**
  - List all income within a date range
  - Example: `list_income("2025-10-01", "2025-10-31")`

### Analysis Tools

- **`get_balance(start_date, end_date)`**
  - Calculate net balance (income - expenses) for a date range
  - Returns: total_income, total_expenses, and balance
  - Example: `get_balance("2025-10-01", "2025-10-31")`

- **`summarize(start_date, end_date, category=None)`**
  - Summarize expenses by category
  - Optionally filter by specific category
  - Example: `summarize("2025-10-01", "2025-10-31")`

## Database Schema

### Expenses Table
```sql
CREATE TABLE expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT DEFAULT '',
    note TEXT DEFAULT ''
)
```

### Income Table
```sql
CREATE TABLE income(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    source TEXT NOT NULL,
    note TEXT DEFAULT ''
)
```

## Example Usage with Claude

Once configured, you can interact with Claude naturally:

```
You: "Add an expense of ₹500 for groceries today"
Claude: [Uses add_expense tool] "I've added your grocery expense of ₹500 for today."

You: "What's my balance for October?"
Claude: [Uses get_balance tool] "For October 2025, you have ₹15,000 in income 
and ₹12,000 in expenses, giving you a balance of ₹3,000."

You: "Show me my spending by category this month"
Claude: [Uses summarize tool] "Here's your spending breakdown for October:
- Food: ₹4,500
- Transport: ₹3,000
- Entertainment: ₹2,500
- Others: ₹2,000"
```

## File Structure

```
.
├── main.py              # MCP server code
├── expenses.db          # SQLite database (auto-created)
├── categories.json      # Optional: predefined categories
└── README.md           # This file
```

## Extending the Project

You can extend this tracker by:
- Adding a web interface for mobile access
- Implementing recurring expenses
- Adding budget limits and alerts
- Creating data visualizations
- Exporting data to CSV/Excel
- Adding multi-currency support

## Requirements

- Python 3.8+
- fastmcp
- sqlite3 (included with Python)

## License

MIT License - feel free to modify and use as you wish!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Support

For issues with:
- **MCP Server**: Check the FastMCP documentation
- **Claude Integration**: Visit Claude Desktop documentation
- **This Project**: Open an issue on the repository