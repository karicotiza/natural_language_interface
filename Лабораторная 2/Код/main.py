import PyPDF2
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras import models
from collections import Counter
from pathlib import Path
from tqdm import tqdm


class Languages:
    languages = {
        "ru": Path("data", "ru.feather"),
        "en": Path("data", "en.feather"),
    }


class SearchImageOfLanguage:
    def __init__(self, path_to_pdf: str, length_threshold: int = 5, amount_threshold: int = 3) -> None:
        self.__search_image = PDF.clean_counter(
            PDF.indexing(
                path_to_pdf,
                length_threshold
            ),
            amount_threshold
        )

    def save_as(self, path_to_index: str):
        data = pd.DataFrame.from_dict(self.__search_image, orient='index').reset_index()
        data.rename(columns={'index': 'word', 0: 'amount'}, inplace=True)
        data["frequency"] = data["amount"] / data["amount"].sum()

        data.to_feather(
            Path("data", (path_to_index + ".feather"))
        )


class SearchImageOfDocument:
    def __init__(self, path_to_pdf: [str | Path], length_threshold: int = 20, amount_threshold: int = 1) -> None:
        self.__search_image = PDF.clean_counter(
            PDF.indexing(
                path_to_pdf,
                length_threshold
            ),
            amount_threshold
        )

    def detect_language(self, mode: str = "short_words") -> dict:
        match mode:
            case "short_words":
                return self.__short_words_method()
            case "alphabet":
                return self.__alphabet_method()
            case "neural":
                return self.__neural_method()
            case _:
                raise ValueError("Wrong mode")

    def __short_words_method(self):
        languages = dict({(key, 1) for key in Languages.languages.keys()})

        for language in languages.keys():
            data = pd.read_feather(Languages.languages[language])
            for key, value in self.__search_image.items():
                if key in list(data["word"]):
                    languages[language] *= float(data[data["word"] == key]["frequency"])

        return languages

    def __alphabet_method(self) -> dict:
        languages = dict({(key, 0) for key in Languages.languages.keys()})

        for key, value in self.__search_image.items():
            for letter in key:
                if 65 <= ord(letter) <= 122:
                    languages["en"] += 1 * value
                elif 1040 <= ord(letter) <= 1103:
                    languages["ru"] += 1 * value

        return languages

    def __neural_method(self):
        model = models.load_model("best_model.hdf5")

        languages = dict((key, 0) for key in Languages.languages)

        with open('tokenizer.pickle', 'rb') as file:
            tokenizer = pickle.load(file)

        for key, value in self.__search_image.items():
            if not key == "'":
                try:
                    word = key
                    my_array = [0 for _ in range(19)]
                    my_array.append(tokenizer.word_index[word])
                    word = np.array(my_array).reshape(1, 20)

                    en, ru = model.predict(word, verbose=False)[0]
                    languages["ru"] += round(ru, 2)
                    languages["en"] += round(en, 2)
                except KeyError:
                    pass

        return languages


class PDF:
    @staticmethod
    def indexing(path_to_pdf: str, length_of_short_words: int) -> Counter:
        search_image = Counter()

        for page in tqdm(
                range(PDF.get_pages(path_to_pdf)),
                desc="indexing"
        ):
            search_image += PDF.count_short_words(
                PDF.get_text_from_page(path_to_pdf, page),
                length_of_short_words,
            )

        return search_image

    @staticmethod
    def count_short_words(text: str, length_threshold: int) -> Counter:
        return Counter(
            [
                word.lower() for
                word in
                text.split() if
                PDF.__is_word(word) and
                len(word) <= length_threshold
            ]
        )

    @staticmethod
    def clean_counter(counter: Counter, amount_threshold: int) -> Counter:
        return Counter(
            [element for element in counter.elements() if counter[element] >= amount_threshold]
        )

    @staticmethod
    def get_text_from_page(path_to_pdf: str, page: int) -> str:
        with open(
                Path(path_to_pdf),
                "rb",
        ) as file:
            return PyPDF2.PdfFileReader(file).getPage(page).extractText()

    @staticmethod
    def get_pages(path_to_pdf: str) -> int:
        with open(
                Path(path_to_pdf),
                "rb",
        ) as file:
            return PyPDF2.PdfFileReader(file).getNumPages()

    @staticmethod
    def __is_word(word: str) -> bool:
        for letter in word:
            if not (letter.isalpha() or letter == "'"):
                return False
        else:
            return True


if __name__ == "__main__":
    # dostoevskiy_idiot = SearchImageOfLanguage("data/Достоевский - Идиот.pdf")
    # dostoevskiy_idiot.save_as("ru")
    # fitzgerald_gatsby = SearchImageOfLanguage("data/Fitzgerald - Gatsby.pdf")
    # fitzgerald_gatsby.save_as("en")

    path = Path("data")
    for file in path.iterdir():
        if file.suffix == ".pdf":
            pdf = SearchImageOfDocument(file)
            print(
                f"Название: {file.name}",
                f"Язык (Метод коротких слов): {pdf.detect_language(mode='short_words')}",
                f"Язык (Алфавитный метод): {pdf.detect_language(mode='alphabet')}",
                f"Язык (Нейросетевой метод): {pdf.detect_language(mode='neural')}",
                f"Ссылка: {file.absolute()}",
                sep="\n",
                end="\n\n"
            )

