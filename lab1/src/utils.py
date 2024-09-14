import re

from prettytable import PrettyTable


def build_query(query_string: str, *, contractions: dict[str, str]) -> dict[str, str]:
    pattern = r'^(\w+:\s*\w+(,\s*\w+:\s*\w+)*)$'
    if not re.match(pattern, query_string):
        raise ValueError('Wrong query string format')
    result: dict = {}
    for condition in query_string.split(','):
        key, value = (string.strip() for string in condition.split(':'))
        if key in contractions:
            result.update({contractions[key]: value})
    return result


def build_format(format_string: str, *, contractions: dict[str, str]) -> tuple[str, ...]:
    result: list[str] = []
    pattern = r'^(\w+(,\s*\w+)*)$'
    if not re.match(pattern, format_string):
        raise ValueError('Wrong format string format')
    for field in format_string.split(','):
        if field in contractions:
            result.append(contractions[field.strip()])
    return tuple(result)


def get_table(objects: list[dict[str, str]]) -> PrettyTable:
    table = PrettyTable()
    table.field_names = objects[0].keys()
    for obj in objects:
        table.add_row(obj.values())
    return table
