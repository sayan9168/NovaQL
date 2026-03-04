from lark import Lark, Transformer, v_args

grammar = r"""
    ?start: pipeline
    pipeline: transform+

    ?transform: "from" table        -> from_table
             | "|" "select" fields  -> select_fields
             | "|" "filter" condition -> filter_cond
             | "|" "group" "by" fields -> group_by
             | "|" "sort" order      -> sort_by

    table: CNAME
    fields: field ("," field)*
    field: CNAME ["." CNAME]        // e.g., orders.amount or customers.name
    
    condition: expr OP expr
    expr: field | NUMBER | STRING
    OP: "==" | ">" | "<" | "!=" | ">=" | "<="
    
    order: field ["desc" | "asc"]

    %import common.CNAME
    %import common.NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

@v_args(inline=True)
class NovaQLCompiler(Transformer):
    def __init__(self):
        self.main_table = ""
        self.joins = set()
        self.select_clause = "*"
        self.where_clauses = []
        self.group_by_clause = ""
        self.order_by_clause = ""

    def from_table(self, table):
        self.main_table = str(table)
        return table

    def field(self, table_or_col, col=None):
        if col:
            table = str(table_or_col)
            column = str(col)
            if table != self.main_table:
                # অটোমেটিক জয়েন ডিটেকশন (ধরে নিচ্ছি foreign key ফরম্যাট: table_id)
                self.joins.add(f"JOIN {table} ON {self.main_table}.{table}_id = {table}.id")
            return f"{table}.{column}"
        return str(table_or_col)

    def select_fields(self, *fields):
        self.select_clause = ", ".join([str(f) for f in fields])
        return self.select_clause

    def filter_cond(self, left, op, right):
        sql_op = "=" if str(op) == "==" else str(op)
        self.where_clauses.append(f"{left} {sql_op} {right}")
        return f"{left} {sql_op} {right}"

    def pipeline(self, items):
        sql = f"SELECT {self.select_clause} FROM {self.main_table}"
        
        if self.joins:
            sql += " " + " ".join(self.joins)
        
        if self.where_clauses:
            sql += f" WHERE {' AND '.join(self.where_clauses)}"
            
        return sql

# --- Test NovaQL ---
parser = Lark(grammar, start='start')

# অ্যাডভান্সড কুয়েরি: অটোমেটিক কাস্টমার টেবিল জয়েন করবে
nova_query = """
from orders
| select orders.id, customers.name, orders.amount
| filter customers.city == "Dhaka"
"""

tree = parser.parse(nova_query)
print("--- NovaQL Smart Compiler Output ---")
print(NovaQLCompiler().transform(tree))
