from collections import Counter


class Word:
    @staticmethod
    def is_word(word: str) -> bool:
        if len(word) > 4:
            for letter in word:
                if letter.isalpha() or letter == "'":
                    pass
                else:
                    return False
            return True
        else:
            return False


class Document:
    def __init__(self, path: str, lang: str) -> None:
        self.__path = path
        self.lang = lang

    def get_text(self) -> str:
        with open(self.__path, mode="r", encoding="utf8") as file:
            return file.read()

    def get_clean_text(self) -> str:
        return self.get_text().replace("\n", " ")

    def get_sentences(self) -> list[str]:
        return self.get_clean_text().split(". ")

    def get_counter(self) -> Counter:
        return Counter(self.get_words())

    def get_words(self):
        return [word.lower() for word in self.get_clean_text().split(" ") if Word.is_word(word)]

    @staticmethod
    def get_len(document) -> int:
        return len(document.get_words())

    @staticmethod
    def list_to_str(list_: list) -> str:
        return str(". ").join(list_)
