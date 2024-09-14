from src.readers import FileReader


class FileSearcher:
    def __init__(self, reader: FileReader):
        self._reader = reader

    def query(self, query: dict, format: tuple[str, ...]) -> list:
        result: list = []
        if not query:
            return result
        for obj in self._reader.read_lines():
            if all(obj.get(query_key) == query_value for query_key, query_value in query.items()):
                filtered_obj = {k: v for k, v in obj.items() if k in format}
                result.append(filtered_obj)
        return result
