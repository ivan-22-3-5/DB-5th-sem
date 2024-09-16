from pathlib import Path

from src import texts
from src.readers import TxtReader
from src.searchers import FileSearcher
from src.utils import build_query, build_format, get_table


def main():
    file = Path('../data/students.txt')
    file_format = ('student_name', 'student_surname', 'grade', 'classroom', 'bus', 'teacher_name', 'teacher_surname')
    contractions = {'sn': 'student_name',
                    'ss': 'student_surname',
                    'g': 'grade',
                    'c': 'classroom',
                    'b': 'bus',
                    'tn': 'teacher_name',
                    'ts': 'teacher_surname'}
    print("Contractions: \n" + '\n'.join([f'{k}: {v}' for k, v in contractions.items()]))
    try:
        query = build_query(input(texts.query_input_request), contractions=contractions)
        result_format_input = input(texts.format_input_request)
        result_format = build_format(result_format_input,
                                     contractions=contractions) if result_format_input.lower() != 'all' else file_format
    except ValueError:
        print("Invalid input format")
        return

    txt_reader = TxtReader(file, file_format)
    searcher = FileSearcher(txt_reader)
    result = searcher.query(query, result_format)
    if not result:
        print("Nothing found")
        return
    for part in list(result[i*50:(i+1)*50] for i in range(0, len(result) // 50+1)):
        print(get_table(part))
        if input(f"Found {len(result)}; Print more? (y/n): ").lower() != 'y':
            break


if __name__ == '__main__':
    main()
