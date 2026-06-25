from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Query:
    columns: List[str]
    filters: Dict[str, str]

def refine_query(query: Query, columns: List[str] = None, filters: Dict[str, str] = None) -> Query:
    if columns:
        query.columns = columns
    if filters:
        query.filters = filters
    return query

def generate_query(query: Query) -> str:
    columns_str = ", ".join(query.columns)
    filters_str = " AND ".join(f"{key} = '{value}'" for key, value in query.filters.items())
    if filters_str:
        return f"SELECT {columns_str} WHERE {filters_str}"
    else:
        return f"SELECT {columns_str}"

def apply_filters(query: Query, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    filtered_data = []
    for row in data:
        match = True
        for key, value in query.filters.items():
            if row.get(key) != value:
                match = False
                break
        if match:
            filtered_data.append(row)
    return filtered_data
