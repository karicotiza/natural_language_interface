from pathlib import Path
from typing import Generator
from collections import Counter
from math import log
from tqdm import tqdm
import pandas as pd


class Spelling:
    __stop_words = ["with", "that", "have", "which", "from", "above", "when", "while"]

    @staticmethod
    def is_word(word: str) -> bool:
        length = len(word)

        if length > 3 and word not in Spelling.__stop_words:
            for letter in word:
                if letter.isalpha():
                    pass
                elif letter == "'" or letter == "-":
                    pass
                else:
                    return False
        else:
            return False

        return True


class Document:
    def __init__(self, text: str) -> None:
        self.__text = text

    def get_text(self):
        return self.__text

    def get_clean_text(self):
        return self.__clean(self.__text)

    @staticmethod
    def __clean(text: str) -> str:
        memory = text
        for digit in [",", ".", "!", "?", ".", "(", ")", "- ", "– ", "— ", ":"]:
            memory = memory.replace(digit, "")

        return memory

    def get_sentences(self) -> Generator:
        return (
            self.__clean(sentence.lower())
            for sentence
            in self.__text.replace("\n", ". ").split(". ")
            if len(sentence) > 3
        )

    def get_counter(self) -> Counter:
        words = (word.lower() for word in self.get_clean_text().split() if Spelling.is_word(word))

        return Counter(word for word in words)

    def get_paragraphs(self):
        return (paragraph for paragraph in self.get_clean_text().split("\n") if paragraph)


class Folder:
    def __init__(self, path: Path = Path("data")):
        if path.is_dir():
            self.path = path
        else:
            raise ValueError("path parameter must be a folder")

    def __iter__(self):
        for file in self.path.iterdir():
            if file.suffix == ".txt":
                yield file.absolute()


class Crawler:
    __columns = ["Name", "Text", "URL"]
    __path = Path("data", "data.csv")

    def __init__(self, folder: Folder):
        self.folder = folder
        self.texts = pd.DataFrame(
            columns=Crawler.__columns
        )

        self.collect()

    def collect(self) -> None:
        for file in tqdm(self.folder, desc="indexing documents"):
            self.texts = pd.concat(
                [
                    self.texts,
                    self.__create_row(
                        self.__extract(file)
                    )
                ],
                ignore_index=True,
            )

            self.__save()

    def __save(self) -> None:
        self.texts.to_csv(Crawler.__path, index=False)

    @staticmethod
    def __create_row(data: [tuple | list]) -> pd.DataFrame:
        return pd.DataFrame(
            columns=Crawler.__columns,
            data=[data]
        )

    @staticmethod
    def __extract(file: Path) -> tuple:
        with file.open(mode='r', encoding='utf-8') as file_:
            text = file_.read().replace("\n\n", "\n")

        return (
            file.stem,
            text,
            file,
        )

    def __get_documents_with_word(self, word: str) -> int:
        memory = 0
        for document in self.texts["Text"]:
            document = Document(document)
            if word in document.get_counter().keys():
                memory += 1

        return memory

    def __get_amount_of_documents(self) -> int:
        return len(self.texts)

    def get_word_scores(self) -> dict:
        scores = {}

        for document in tqdm(self.texts["Text"], desc="calculating word scores"):
            document = Document(document)

            for word in document.get_counter():
                memory = {
                    "word": word,
                    "in sentence": 0,
                    "in document": document.get_counter()[word],
                    "documents amount with word": self.__get_documents_with_word(word),
                    "max frequency": max(document.get_counter().values()),
                    "document amount": self.__get_amount_of_documents(),
                }

                score = 0

                for sentence in document.get_sentences():
                    if memory["word"] in sentence:
                        memory["in sentence"] += len([word for word in sentence.split() if word == memory["word"]])

                    score += (memory["in sentence"] / len(sentence.split())) * (
                            0.5 *
                            (1 + memory["in document"] / memory["max frequency"]) *
                            log(memory["document amount"] / memory["documents amount with word"])
                    )

                    memory["in sentence"] = 0

                scores[memory["word"]] = round(score, 3)

        return scores

    def __get_sentence_scores(self) -> Generator:
        word_scores = self.get_word_scores()

        for document in self.texts["Text"]:
            sentence_scores = {}
            document = Document(document)

            memory = {
                "letters amount": sum(len(sentence) for sentence in document.get_sentences()),
                "letters before": 0,
                "letters in paragraph": 0,
                "letters before sentence in paragraph": 0,
            }

            for sentence in document.get_sentences():
                score = 0

                for paragraph in document.get_paragraphs():
                    if sentence in paragraph.lower():
                        memory["letters in paragraph"] = len(paragraph)
                        break
                    else:
                        memory["letters before sentence in paragraph"] += len(sentence)

                for word in (word for word in sentence.split() if Spelling.is_word(word)):
                    score += (
                            word_scores[word] *
                            (1 - (memory["letters before"] / memory["letters amount"])) *
                            (1 - (memory["letters before sentence in paragraph"] / memory["letters in paragraph"]))
                    )

                sentence_scores[sentence] = score

                memory["letters before"] += len(sentence)
                memory["letters in paragraph"] = 0
                memory["letters before sentence in paragraph"] = 0

            yield (
                self.texts[self.texts["Text"] == document.get_text()]["Name"].values[0],
                sentence_scores
            )

    def get_summaries(self) -> Generator:
        for name, scores in self.__get_sentence_scores():
            scores = sorted(scores, key=scores.get, reverse=True)[:10]
            memory = [name]
            for document in self.texts["Text"]:
                for sentence in document.replace("\n", ". ").split(". "):
                    original = sentence
                    converted = Document(sentence).get_clean_text().lower()
                    if converted in scores:
                        memory.append(original)
            string = ""
            for index, sentence in enumerate(memory):
                if index == 0:
                    string += f"Название: {sentence}\n"
                else:
                    string += f"#{index}: {sentence}.\n".replace("..", ".")
            url = str(self.texts[self.texts["Name"] == name]["URL"].values[0])
            string += f"Ссылка: {url}\n"

            yield string
