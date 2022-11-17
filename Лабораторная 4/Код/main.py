import tkinter
import os

from models import OpusMTEnRu, WMT19RuEn
from document import Document, Word
from nlp import SyntaxTree, POS
from collections import Counter
from tkinter.scrolledtext import ScrolledText
from pathlib import Path


class Pipeline:
    def __init__(self):
        self.__ru_to_en = WMT19RuEn()
        self.__en_to_ru = OpusMTEnRu()

        self.__files = {
            # "Мы в ответе за тех, кого приручили": Document("data/Мы в ответе.txt", "ru"),
            "How does GRU work?": Document("data/gru.txt", "en"),
        }

    @staticmethod
    def __get_length(document: Document) -> str:
        return f"Length: {Document.get_len(document)} words\n"

    def __get_translation(self, document: Document, language: str) -> list[str]:
        if language == "ru":
            translation = [self.__ru_to_en.predict(sentence) for sentence in document.get_sentences()]
        else:
            translation = [self.__en_to_ru.predict(sentence) for sentence in document.get_sentences()]
        return translation

    @staticmethod
    def __get_translated_len(translation: list[str]) -> str:
        translated_len = len(
            [word.lower() for word in Document.list_to_str(translation).split(" ") if Word.is_word(word)])
        return f"Translation Length: {translated_len} words\n"

    @staticmethod
    def __get_frequency(document: Document) -> Counter:
        return document.get_counter()

    def __get_words(self, frequency: Counter, language: str) -> str:
        memory = ""

        for index, items in enumerate(frequency.most_common()):
            word, amount = items
            if language == "ru":
                translated_word = self.__ru_to_en.predict(word)
                memory += f"  {index}. {word : <20} | {amount: >3} | {translated_word: <20} | " \
                          f"{POS.get_pos(translated_word)}\n "
            else:
                translated_word = self.__en_to_ru.predict(word)
                memory += f"  {index}. {word : <20} | {amount: >3} | {translated_word: <20} | {POS.get_pos(word)}\n"

        return memory

    @staticmethod
    def __get_sentences(document: Document, language: str, translation: list[str]) -> str:
        memory = f"Sentences:\n"

        if language == "ru":
            for index, sentence in enumerate(translation):
                memory += f"  {index}. {sentence}\n"
                memory += SyntaxTree.make_tree(sentence) + "\n"
        else:
            for index, sentence in enumerate(document.get_sentences()):
                memory += f"  {index}. {sentence}\n"
                memory += SyntaxTree.make_tree(sentence) + "\n"
        memory += "\n\n"

        return memory

    def extract(self):
        for name, document in self.__files.items():
            memory = ""

            language = document.lang
            translation = self.__get_translation(document, language)
            frequency = self.__get_frequency(document)

            memory += f"File: {name}\n\n"
            memory += self.__get_length(document)
            memory += self.__get_translated_len(translation)

            for index, line in enumerate(translation):
                memory += f"  {index}. {line}\n"
            memory += "\n"

            memory += f"Frequency: {str(frequency)}\n"
            memory += self.__get_words(frequency, language) + "\n"

            memory += self.__get_sentences(document, language, translation)

            yield memory


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Перевод")

        self._ = tkinter.Label(text="Путь к папке")
        self._.grid(
            row=0,
            column=0,
        )

        self.path = tkinter.Entry(
            width=80,
        )
        self.path.grid(
            row=0,
            column=1,
        )

        self.help = tkinter.Button(
            text="Помощь",
            command=self.__help,
            width=40,
        )
        self.help.grid(
            row=1,
            column=0,
            columnspan=2,
        )

        self.classic = tkinter.Button(
            text="Перевод+",
            command=self.__translate,
            width=40,
        )
        self.classic.grid(
            row=2,
            column=0,
            columnspan=2,
        )

        self.output = ScrolledText(
            width=180
        )

        self.output.grid(
            row=5,
            column=0,
            columnspan=2,
        )

        self.window.mainloop()

    def __print(self, text):
        self.output.insert(
            tkinter.INSERT,
            text + "\n"
        )

    @staticmethod
    def __save(path: str, text: str):
        if not os.path.exists("saved"):
            os.makedirs("saved")
        path_ = Path("saved", (path + ".txt"))
        with open(path_, mode="w", encoding="utf-8") as file_:
            file_.write(text)

    def __get_path(self):
        return Path(self.path.get())

    def __help(self):
        self.__print(
            "Введите путь к папке в которой находятся файлы с расширением '.txt'\n" +
            "После этого нажмите кнопку 'перевод+'\n" +
            "Результаты работы программы появятся в поле ниже\n" +
            "Текст выведенный ниже - активный, его можно копировать и редактировать\n" +
            "Вы получите перевод по предложениям;\n" +
            "Разбор слов (слово | количество в документе | перевод | часть речи)';\n" +
            "Синтаксический разбор предложений, соответственно\n"
        )

    def __translate(self):
        pipeline = Pipeline()
        for summary in pipeline.extract():
            self.__print(summary)
            self.__save(
                "extracted",
                summary
            )


if __name__ == "__main__":
    window = Window()
