from pathlib import Path

from src.readers import TxtReader
from src.searchers import FileSearcher


def main():
    file = Path('../data/students.txt')
    file_format = ('student_name', 'student_surname', 'grade', 'classroom', 'bus', 'teacher_name', 'teacher_surname')

    txt_reader = TxtReader(file, file_format)
    searcher = FileSearcher(txt_reader)

    query = {'teacher_name': 'FAFARD', 'teacher_surname': 'ROCIO'}
    result_format = ('student_name', 'student_surname', 'teacher_name', 'teacher_surname')

    print(searcher.query(query, result_format))


if __name__ == '__main__':
    main()
