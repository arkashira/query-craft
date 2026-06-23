import pytest
from query_craft import QueryCraft, DatabaseConnection, Template, create_setup_wizard

def test_add_database_connection():
    query_craft = QueryCraft()
    connection = DatabaseConnection(
        host="localhost",
        username="username",
        password="password",
        database="database"
    )
    query_craft.add_database_connection(connection)
    assert len(query_craft.database_connections) == 1

def test_add_template():
    query_craft = QueryCraft()
    template = Template(
        name="template1",
        query="SELECT * FROM table1"
    )
    query_craft.add_template(template)
    assert len(query_craft.templates) == 1

def test_execute_sample_query():
    query_craft = QueryCraft()
    connection = DatabaseConnection(
        host="localhost",
        username="username",
        password="password",
        database="database"
    )
    query_craft.add_database_connection(connection)
    template = Template(
        name="template1",
        query="SELECT * FROM table1"
    )
    query_craft.add_template(template)
    result = query_craft.execute_sample_query()
    assert result == "Sample query executed successfully"

def test_execute_sample_query_no_connections():
    query_craft = QueryCraft()
    with pytest.raises(ValueError):
        query_craft.execute_sample_query()

def test_execute_sample_query_no_templates():
    query_craft = QueryCraft()
    connection = DatabaseConnection(
        host="localhost",
        username="username",
        password="password",
        database="database"
    )
    query_craft.add_database_connection(connection)
    with pytest.raises(ValueError):
        query_craft.execute_sample_query()

def test_get_tutorial_links():
    query_craft = QueryCraft()
    links = query_craft.get_tutorial_links()
    assert len(links) == 2
    assert links[0] == "https://example.com/tutorial1"
    assert links[1] == "https://example.com/tutorial2"

def test_create_setup_wizard():
    query_craft = create_setup_wizard()
    assert len(query_craft.database_connections) == 1
    assert len(query_craft.templates) == 1
