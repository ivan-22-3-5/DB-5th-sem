from pathlib import Path


class FileSearcher:
    def __init__(self, file: Path, format: tuple[str, ...]):
        self._file = file
        self._format = format

    def _read(self) -> dict:
        with open(self._file) as f:
            while line := f.readline():
                yield {k: v for k, v in zip(self._format, line.strip().split(','))}

    def query(self, query: dict, format: tuple[str, ...]) -> list:
        result: list = []
        for obj in self._read():
            if all(obj.get(query_key) == query_value for query_key, query_value in query.items()):
                filtered_obj = {k: v for k, v in obj.items() if k in format}
                result.append(filtered_obj)
        return result


def main():
    file = Path('../data/students.txt')
    format = ('student_name', 'student_surname', 'grade', 'classroom', 'bus', 'teacher_name', 'teacher_surname')
    searcher = FileSearcher(file, format)

    print(searcher.query({'teacher_name': 'FAFARD', 'teacher_surname': 'ROCIO'}, ('student_name', 'student_surname', 'teacher_name', 'teacher_surname')))


if __name__ == '__main__':
    main()
