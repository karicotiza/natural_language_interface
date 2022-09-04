import math
import pandas as pd
import preprocessing
import warnings
import wikipedia

from tqdm import tqdm


class Crawler:
    def __init__(self, attempts: int) -> None:
        self.columns = ["Title", "URL", "Summary"]
        self.database = pd.DataFrame(
            columns=self.columns,
        )

        # wikipedia module troubles
        warnings.catch_warnings()
        warnings.simplefilter("ignore")

        self.crawl(attempts)
        self.database.fillna(0, inplace=True)
        self.set_weights()
        self.save_database()

    def crawl(self, attempts: int) -> None:
        for page_id in tqdm(range(attempts), desc="indexing"):
            try:
                page = wikipedia.page(pageid=page_id)
                if preprocessing.is_article(page.title):
                    main_data = pd.DataFrame(
                        columns=self.columns,
                        data=[
                            [page.title, page.url, page.summary],
                        ]
                    )

                    tokenized_sentence = self.tokenize(
                        main_data["Summary"].iat[-1]
                    )

                    indexing_data = pd.DataFrame(
                        columns=tokenized_sentence.keys(),
                        data=[tokenized_sentence.values()],
                        dtype=pd.Int8Dtype
                    )

                    data = pd.concat([main_data, indexing_data], axis=1, ignore_index=False)

                    self.database = pd.concat([self.database, data], axis=0, ignore_index=True)

            # wikipedia module troubles
            except AttributeError:
                pass
            except wikipedia.exceptions.PageError:
                pass
            except wikipedia.DisambiguationError:
                pass

    @staticmethod
    def tokenize(sentence: str) -> dict:
        sentence = preprocessing.normalize(sentence)

        frequency = dict(
            (word, sentence.count(word)) for word in set(sentence)
        )

        return frequency

    def set_weights(self) -> None:
        counter = 0
        for column in tqdm(self.database.columns[len(self.columns):], desc="calculating weights"):
            counter += 1

            coefficient = math.log(len(self.database) / len(self.database[self.database[column] > 0]))
            self.database[column] *= coefficient

    def save_database(self) -> None:
        tqdm(self.database.to_feather("data.feather"), desc="saving")


crawler = Crawler(5000)
