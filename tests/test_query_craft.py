from query_craft import Query, refine_query, generate_query, apply_filters

def test_refine_query():
    query = Query(columns=["name", "age"], filters={"age": "25"})
    refined_query = refine_query(query, columns=["name", "email"])
    assert refined_query.columns == ["name", "email"]
    assert refined_query.filters == {"age": "25"}

def test_refine_query_filters():
    query = Query(columns=["name", "age"], filters={"age": "25"})
    refined_query = refine_query(query, filters={"age": "30"})
    assert refined_query.columns == ["name", "age"]
    assert refined_query.filters == {"age": "30"}

def test_generate_query():
    query = Query(columns=["name", "age"], filters={"age": "25"})
    generated_query = generate_query(query)
    assert generated_query == "SELECT name, age WHERE age = '25'"

def test_generate_query_no_filters():
    query = Query(columns=["name", "age"], filters={})
    generated_query = generate_query(query)
    assert generated_query == "SELECT name, age"

def test_apply_filters():
    query = Query(columns=["name", "age"], filters={"age": "25"})
    data = [
        {"name": "John", "age": "25"},
        {"name": "Jane", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    filtered_data = apply_filters(query, data)
    assert len(filtered_data) == 2
    assert filtered_data[0]["name"] == "John"
    assert filtered_data[1]["name"] == "Bob"

def test_apply_filters_no_match():
    query = Query(columns=["name", "age"], filters={"age": "40"})
    data = [
        {"name": "John", "age": "25"},
        {"name": "Jane", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    filtered_data = apply_filters(query, data)
    assert len(filtered_data) == 0
