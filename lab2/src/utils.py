import re
from itertools import product

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
        if field.strip() in contractions:
            result.append(contractions[field.strip()])
    return tuple(result)


def join_results(first_query_result: list[dict[str, str]],
                 second_query_result: list[dict[str, str]],
                 *, join_by: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for first, second in product(first_query_result, second_query_result):
        try:
            if first[join_by] == second[join_by]:
                result.append({**first, **second})
        except KeyError:
            pass
    return result


def get_table(objects: list[dict[str, str]], fields: tuple[str, ...]) -> PrettyTable:
    table = PrettyTable()
    table.field_names = fields
    for obj in objects:
        table.add_row([value for key, value in obj.items() if key in fields])
    return table
