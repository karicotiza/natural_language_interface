from pathlib import Path


class Folder:
    def __init__(self, path: str):
        self.__path = Path(path)

    def __iter__(self):
        for file in self.__path.iterdir():
            if file.suffix == ".txt":
                yield file.stem


class Document:
    def __init__(self, path: str):
        self.__path = Path(path)

    def __iter__(self):
        with open(self.__path, mode="r", encoding="utf-8") as file:
            for line in file.read().split("\n"):
                yield line
