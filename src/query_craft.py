from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class Query:
    name: str
    parameter_schema: Dict[str, str]
    result_schema: Dict[str, str]

class QueryCraft:
    def __init__(self):
        self.queries = [
            Query("example_query", {"param1": "str", "param2": "int"}, {"result1": "str", "result2": "int"}),
        ]

    def list_queries(self):
        return [query.name for query in self.queries]

    def get_query(self, query_name):
        for query in self.queries:
            if query.name == query_name:
                return query
        return None

    def run_query(self, query_name, params):
        query = self.get_query(query_name)
        if query:
            # Simulate running the query
            result = {"result1": f"{params['param1']} - {params['param2']}", "result2": 42}
            return result
        return None

    def render_query_form(self, query_name):
        query = self.get_query(query_name)
        if query:
            form = f"<form><h2>{query_name}</h2>"
            for param, param_type in query.parameter_schema.items():
                form += f"<label>{param} ({param_type})</label><br><input type='text' name='{param}'><br>"
            form += "<input type='submit' value='Run'>"
            return form
        return None

    def render_query_results(self, query_name, result):
        table = f"<h2>{query_name} Results</h2><table border='1'>"
        for key, value in result.items():
            table += f"<tr><th>{key}</th><td>{value}</td></tr>"
        table += "</table>"
        return table
