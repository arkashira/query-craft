from query_craft import QueryCraft, Query
import pytest

def test_list_queries():
    craft = QueryCraft()
    queries = craft.list_queries()
    assert len(queries) == 1
    assert queries[0] == "example_query"

def test_get_query():
    craft = QueryCraft()
    query = craft.get_query("example_query")
    assert query.name == "example_query"
    assert query.parameter_schema == {"param1": "str", "param2": "int"}

def test_run_query():
    craft = QueryCraft()
    result = craft.run_query("example_query", {"param1": "hello", "param2": "42"})
    assert result == {"result1": "hello - 42", "result2": 42}

def test_render_query_form():
    craft = QueryCraft()
    form = craft.render_query_form("example_query")
    assert "<form>" in form
    assert "<label>param1 (str)</label>" in form
    assert "<label>param2 (int)</label>" in form

def test_render_query_results():
    craft = QueryCraft()
    result = {"result1": "hello - 42", "result2": 42}
    table = craft.render_query_results("example_query", result)
    assert "<h2>example_query Results</h2>" in table
    assert "<th>result1</th><td>hello - 42</td>" in table
    assert "<th>result2</th><td>42</td>" in table

def test_get_query_not_found():
    craft = QueryCraft()
    query = craft.get_query("non_existent_query")
    assert query is None

def test_run_query_not_found():
    craft = QueryCraft()
    result = craft.run_query("non_existent_query", {"param1": "hello", "param2": "42"})
    assert result is None
