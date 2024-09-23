from datetime import datetime
from pathlib import Path

from src import texts
from src.readers import TxtReader
from src.searchers import FileSearcher
from src.utils import build_query, build_format, get_table, join_results


def main():
    students_file = Path('data/students.txt')
    teachers_file = Path('data/teachers.txt')

    students_file_format = ('student_name', 'student_surname', 'grade', 'classroom', 'bus')
    teachers_file_format = ('teacher_name', 'teacher_surname', 'classroom')

    all_fields = ('student_name', 'student_surname', 'grade', 'classroom', 'bus', 'teacher_name', 'teacher_surname')

    students_contractions = {'sn': 'student_name',
                             'ss': 'student_surname',
                             'g': 'grade',
                             'c': 'classroom',
                             'b': 'bus', }

    teachers_contractions = {'c': 'classroom',
                             'tn': 'teacher_name',
                             'ts': 'teacher_surname'}

    print("Contractions: \n" + '\n'.join(
        [f'{k}: {v}' for k, v in {**students_contractions, **teachers_contractions}.items()]))
    try:

        query_input = input(texts.query_input_request)

        students_query = build_query(query_input,
                                     contractions=students_contractions)
        teachers_query = build_query(query_input,
                                     contractions=teachers_contractions)

        result_format_input = input(texts.format_input_request)

        result_format = build_format(result_format_input,
                                     contractions={**students_contractions,
                                                   **teachers_contractions}) if result_format_input.lower() != 'all' else all_fields

    except ValueError:
        print("Invalid input format")
        return

    students_reader = TxtReader(students_file, students_file_format)
    teachers_reader = TxtReader(teachers_file, teachers_file_format)

    students_searcher = FileSearcher(students_reader)
    teachers_searcher = FileSearcher(teachers_reader)

    start_time = datetime.now()
    students_result = students_searcher.query(students_query, students_file_format)
    teachers_result = teachers_searcher.query(teachers_query, teachers_file_format)
    result = join_results(students_result, teachers_result, join_by='classroom')
    end_time = datetime.now()

    if not result:
        print("Nothing found")
        return

    print(f"Time elapsed: {end_time - start_time}")

    for i in range(0, len(result), 20):
        part = result[i:i + 20]
        print(get_table(part, result_format))

        if input(f"Found {len(result)}; Print more? (y/n): ").lower() != 'y':
            break


if __name__ == '__main__':
    main()
