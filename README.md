# NovaQL

### Next-gen pipelined query language — cleaner than nested SQL

Readable pipelines · Smart joins · Implicit grouping · Compiles to SQL

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Parser](https://img.shields.io/badge/Parser-Lark-green)](https://github.com/lark-parser/lark)

> Write queries top-to-bottom with `|` pipes instead of deeply nested SQL.

---

## Why NovaQL?

SQL gets messy with nested subqueries and repetitive `JOIN` / `GROUP BY` boilerplate.  
NovaQL uses a **pipeline architecture** so data flows clearly from stage to stage.

### Highlights

- **Pipelined syntax** — logic reads top → bottom
- **Smart joins** — dot notation can drive relationship handling (e.g. `customers.name`)
- **Implicit grouping** — less repetitive column listing
- **Intuitive filters** — operators like `==`

---

## SQL vs NovaQL

**SQL**
```sql
SELECT orders.id, customers.name, orders.amount
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE customers.city = 'Dhaka';
```

**NovaQL**
```text
from orders
| select orders.id, customers.name, orders.amount
| filter customers.city == "Dhaka"
```

---

## Install

```bash
pip install lark
git clone https://github.com/sayan9168/NovaQL.git
cd NovaQL
```

---

## Basic usage

```python
from novaql import parser, NovaQLCompiler

query = """
from sales
| filter amount >= 500
| group by region
"""

tree = parser.parse(query)
sql_output = NovaQLCompiler().transform(tree)
print(sql_output)
```

---

## Project structure

```text
grammar.lark   # Core grammar
compiler.py    # NovaQL → SQL transformer
tests/         # Sample queries
```

---

## Author

[Sayan Mahata](https://github.com/sayan9168)
