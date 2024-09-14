from pathlib import Path

from src.readers import TxtReader
from src.searchers import FileSearcher


def build_query(query_string: str, *, contractions: dict[str, str]) -> dict[str, str]:
    query: dict = {}
    for condition in query_string.split(','):
        key, value = (string.strip() for string in condition.split(':'))
        if key in contractions:
            query.update({contractions[key]: value})
    return query


def build_format(format_string: str, *, contractions: dict[str, str]) -> tuple[str, ...]:
    format: list[str] = []
    for field in format_string.split(','):
        if field in contractions:
            format.append(contractions[field.strip()])
    return tuple(format)


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
    contractions_string = '\n'.join([f'{k}: {v}' for k, v in contractions.items()])
    print("Contractions: \n" + contractions_string)
    query_string = ("Hint: if you want to find all records"
                    "where student_name is 'QWERTY' and classroom is '123' you should write 'sn: QWERTY, c: 123'"
                    "\nWrite your query: ")
    result_format_string = ("Hint: if you want to obtain only specified fields you should write them,"
                            "otherwise put 'all'"
                            "\ne.g. if you want to retrieve only student_name and bus you should write 'sn, b':\n")
    query = build_query(input(query_string), contractions=contractions)
    result_format_input = input(result_format_string)
    result_format = build_format(result_format_input,
                                 contractions=contractions) if result_format_input.lower() != 'all' else file_format
    print(searcher.query(query, result_format))


if __name__ == '__main__':
    main()
