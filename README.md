# 🚀 NovaQL (Next-Gen Query Language)

**NovaQL** is a high-level, pipelined query language designed to be more intuitive and powerful than standard SQL. It focuses on readability, modularity, and automation.

## ✨ Why NovaQL?

SQL often becomes messy with deeply nested subqueries and repetitive `JOIN` statements. NovaQL simplifies data manipulation by using a **pipe-based (`|`) architecture**, similar to modern data processing frameworks.

### Key Features:
- **Pipelined Syntax:** Data flows from top to bottom, making logic easy to follow.
- **Smart Joins:** Automatically detects and handles relationships based on dot notation (e.g., `customers.name` auto-joins the customers table).
- **Implicit Grouping:** No more repetitive column listing in `GROUP BY`.
- **Cleaner Filters:** Uses intuitive operators like `==` for comparisons.

---

## 🛠️ Comparison: SQL vs. NovaQL

### Standard SQL
```sql
SELECT orders.id, customers.name, orders.amount 
FROM orders 
JOIN customers ON orders.customer_id = customers.id 
WHERE customers.city = 'Dhaka';
NovaQL (Much Cleaner!)
from orders
| select orders.id, customers.name, orders.amount
| filter customers.city == "Dhaka"
🚀 Getting Started
NovaQL is built using the Lark parsing toolkit in Python.
Prerequisites
pip install lark
Basic Usage
from novaql import parser, NovaQLCompiler

query = """
from sales
| filter amount >= 500
| group by region
"""

tree = parser.parse(query)
sql_output = NovaQLCompiler().transform(tree)
print(sql_output)
🏗️ Project Structure
grammar.lark: The core grammar definitions.
compiler.py: The Transformer logic that converts NovaQL to optimized SQL.
tests/: Sample queries and test cases.
👤 Author
Developed by Sayan.
