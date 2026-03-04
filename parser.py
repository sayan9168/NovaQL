from lark import Lark, Transformer, v_args

grammar = r"""
    ?start: pipeline

    pipeline: transform+

    ?transform: "from" table        -> from_table
             | "|" "filter" condition -> filter_cond
             | "|" "group" "by" fields -> group_by
             | "|" "aggregate" aggs  -> aggregate
             | "|" "sort" order      -> sort_by

    table: CNAME
    condition: expr OP expr
    fields: CNAME ("," CNAME)*
    aggs: agg ("," agg)*
    agg: CNAME ":" func "(" expr ")"
    func: "sum" | "avg" | "count"
    order: CNAME
    expr: CNAME | NUMBER | STRING
    OP: "==" | ">" | "<" | "!="

    %import common.CNAME
    %import common.NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

@v_args(inline=True)
class ToSql(Transformer):
    def __init__(self):
        self.table_name = ""
        self.filters = []
        self.group_fields = []
        self.aggregations = []

    def from_table(self, table):
        self.table_name = str(table)
        return f"FROM {table}"

    def filter_cond(self, left, op, right):
        # SQL-এ '==' এর বদলে '=' ব্যবহার করা হয়
        sql_op = "=" if str(op) == "==" else str(op)
        self.filters.append(f"{left} {sql_op} {right}")
        return f"WHERE {left} {sql_op} {right}"

    def group_by(self, *fields):
        # কমা দিয়ে ফিল্ডগুলোকে আলাদা করা
        field_list = ", ".join([str(f) for f in fields])
        self.group_fields.append(field_list)
        return f"GROUP BY {field_list}"

    def pipeline(self, items):
        # চুড়ান্ত SQL কুয়েরি অ্যাসেম্বল করা
        select_clause = "*"
        if self.group_fields:
            # Group by থাকলে সাধারণত সেই ফিল্ডগুলো সিলেক্টে থাকতে হয়
            select_clause = ", ".join(self.group_fields)
        
        sql = f"SELECT {select_clause} FROM {self.table_name}"
        
        if self.filters:
            sql += f" WHERE {' AND '.join(self.filters)}"
        
        if self.group_fields:
            sql += f" GROUP BY {', '.join(self.group_fields)}"
            
        return sql

# পার্সার সেটআপ
parser = Lark(grammar, start='start')

# আপনার টেস্ট কুয়েরি
test_query = """
from orders
| filter amount > 1000
| group by category
"""

try:
    tree = parser.parse(test_query)
    result = ToSql().transform(tree)
    print("--- NovaQL Result ---")
    print(result)
except Exception as e:
    print(f"Error parsing NovaQL: {e}")
    
