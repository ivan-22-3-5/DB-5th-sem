from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator


class FileReader(ABC):
    def __init__(self, file: Path, format: tuple[str, ...]):
        self._file = file
        self._format = format

    @abstractmethod
    def read_lines(self) -> Generator[dict, None, None]:
        pass


class TxtReader(FileReader):
    def read_lines(self) -> Generator[dict, None, None]:
        with open(self._file) as f:
            while line := f.readline():
                yield {k: v for k, v in zip(self._format, line.strip().split(','))}