"""
flaskr.utils.node
~~~~~~~~~~~~~~~~~
Utilities for Node structure.
"""
from sqlite3 import Row, Cursor
from typing import List, Union, Iterable


class Node:
    """
    Node Structure for loading data from CTE sql.
    """
    def __init__(self, row_, parent=None, children=None):
        self.row = dict(row_)
        self.parent = parent
        if not children:
            self.children = []

    def __repr__(self):
        return f"{self.row['id']} {self.row['parent_id']}"

    @classmethod
    def build_from_cte_rows(cls, cte_rows: Union[Cursor, List[Row]]) -> Iterable["Node"]:
        root = {}
        rst = {}
        for row in cte_rows:
            rst[row['id']] = cls(row, parent=rst[row['parent_id']] if row['parent_id'] else None)
            if row['parent_id'] is None:
                root[row['id']] = rst[row['id']]
            else:
                rst[row['parent_id']].children.append(rst[row['id']])
        return root.values()
