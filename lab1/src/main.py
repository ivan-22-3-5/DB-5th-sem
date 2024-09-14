import re
from pathlib import Path

from prettytable import PrettyTable

from src.readers import TxtReader
from src.searchers import FileSearcher


def build_query(query_string: str, *, contractions: dict[str, str]) -> dict[str, str]:
    pattern = r'^(\w+:\s*\w+(,\s*\w+:\s*\w+)*)$'
    if not re.match(pattern, query_string):
        raise ValueError('Wrong query string format')
    query: dict = {}
    for condition in query_string.split(','):
        key, value = (string.strip() for string in condition.split(':'))
        if key in contractions:
            query.update({contractions[key]: value})
    return query


def build_format(format_string: str, *, contractions: dict[str, str]) -> tuple[str, ...]:
    format: list[str] = []
    pattern = r'^(\w+(,\s*\w+)*)$'
    if not re.match(pattern, format_string):
        raise ValueError('Wrong format string format')
    for field in format_string.split(','):
        if field in contractions:
            format.append(contractions[field.strip()])
    return tuple(format)


def get_table(objects: list[dict[str, str]]) -> PrettyTable:
    table = PrettyTable()
    table.field_names = objects[0].keys()
    for obj in objects:
        table.add_row(obj.values())
    return table


def main():
    file = Path('../data/students.txt')
    file_format = ('student_name', 'student_surname', 'grade', 'classroom', 'bus', 'teacher_name', 'teacher_surname')

    txt_reader = TxtReader(file, file_format)
    searcher = FileSearcher(txt_reader)

    contractions = {'sn': 'student_name',
                    'ss': 'student_surname',
                    'g': 'grade',
                    'c': 'classroom',
                    'b': 'bus',
                    'tn': 'teacher_name',
                    'ts': 'teacher_surname'}
    print("Contractions: \n" + '\n'.join([f'{k}: {v}' for k, v in contractions.items()]))
    query_input_request_text = ("Hint: if you want to find all records"
                                "where student_name is 'QWERTY' and classroom is '123' "
                                "you should write 'sn: QWERTY, c: 123'"
                                "\nWrite your query: ")
    result_format_input_request_text = ("Hint: if you want to obtain only specified fields you should write them,"
                                        "otherwise put 'all'"
                                        "\ne.g. if you want to retrieve only student_name and bus "
                                        "you should write 'sn, b':\n")
    query = build_query(input(query_input_request_text), contractions=contractions)

    result_format_input = input(result_format_input_request_text)
    result_format = build_format(result_format_input,
                                 contractions=contractions) if result_format_input.lower() != 'all' else file_format
    print(get_table(searcher.query(query, result_format)))


if __name__ == '__main__':
    main()
