"""
flaskr.utils.encoder
~~~~~~~~~~~~~~~~~~~~
Utilities for JSONEncoder.
"""
from flask import json
from typing import Any
from datetime import datetime, timezone

from flaskr.utils.node import Node


class JsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.replace(tzinfo=timezone.utc).timestamp()
        if isinstance(o, Node):
            # Recursion for Node serialization
            o.row['children'] = [self.default(child) for child in o.children]
            return o.row
