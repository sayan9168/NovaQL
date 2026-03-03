from lark import Lark, Transformer, v_args

grammar = r"""
    ?start: pipeline

    pipeline: transform*

    transform: "from" table
             | "|" "filter" condition
             | "|" "group" "by" fields
             | "|" "aggregate" aggs
             | "|" "sort" order

    table: CNAME
    condition: expr OP expr
    fields: CNAME ("," CNAME)*
    aggs: agg ("," agg)*
    agg: CNAME ":" func "(" expr ")"
    func: "sum" | "avg" | "count"
    expr: CNAME | NUMBER | STRING
    OP: "==" | ">" | "<" | "!="

    %import common.CNAME
    %import common.NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, start='start')

@v_args(inline=True)
class ToSql(Transformer):
    def pipeline(self, items):
        sql_parts = []
        current_from = ""
        for item in items:
            if isinstance(item, str) and item.startswith("from "):
                current_from = item.split(" ", 1)[1]
                sql_parts.append(f"SELECT * FROM {current_from}")
            # add logic for filter, group etc.
        return "\n".join(sql_parts)

# Test
tree = parser.parse("""
from orders
| filter amount > 1000
| group by category
""")
print(ToSql().transform(tree))
