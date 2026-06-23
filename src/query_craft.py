import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DatabaseConnection:
    host: str
    username: str
    password: str
    database: str

@dataclass
class Template:
    name: str
    query: str

class QueryCraft:
    def __init__(self):
        self.database_connections = []
        self.templates = []

    def add_database_connection(self, connection: DatabaseConnection):
        self.database_connections.append(connection)

    def add_template(self, template: Template):
        self.templates.append(template)

    def execute_sample_query(self):
        if not self.database_connections:
            raise ValueError("No database connections available")
        if not self.templates:
            raise ValueError("No templates available")
        # Simulate a sample query execution
        return "Sample query executed successfully"

    def get_tutorial_links(self):
        return ["https://example.com/tutorial1", "https://example.com/tutorial2"]

def create_setup_wizard():
    query_craft = QueryCraft()
    # Simulate a guided setup wizard
    database_connection = DatabaseConnection(
        host="localhost",
        username="username",
        password="password",
        database="database"
    )
    query_craft.add_database_connection(database_connection)
    template = Template(
        name="template1",
        query="SELECT * FROM table1"
    )
    query_craft.add_template(template)
    return query_craft
