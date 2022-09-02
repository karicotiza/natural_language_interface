import nltk
import wikipedia
import pandas as pd


class Crawler:
    def __init__(self, attempts: int) -> None:
        self.columns = ["Title", "URL", "Summary"]
        self.database = pd.DataFrame(
            columns=self.columns,
        )

        self.crawl(attempts)
        self.database.fillna(0, inplace=True)
        self.save_database()

    def crawl(self, attempts: int) -> None:
        for page_id in range(attempts):
            try:
                page = wikipedia.page(pageid=page_id)
                print(f"Страница {page_id} - {page.title}")

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

            except AttributeError:
                print(f"Страница {page_id} не существует")
            except wikipedia.exceptions.PageError:
                print(f"Страница {page_id} не существует")
            except wikipedia.DisambiguationError:
                print(f"Страница {page_id} не существует")

    @staticmethod
    def tokenize(sentence: str) -> dict:
        valid_parts_of_speech = ["NN", "NNS", "NNP", "NNPS"]

        tokenizer = nltk.TweetTokenizer()
        lemmatizer = nltk.wordnet.WordNetLemmatizer()

        sentence = tokenizer.tokenize(sentence)
        sentence = [
            word for word in sentence if nltk.pos_tag([word])[0][1] in valid_parts_of_speech
        ]
        sentence = [lemmatizer.lemmatize(word).lower() for word in sentence]

        frequency = dict(
            (word, sentence.count(word)) for word in set(sentence)
        )

        return frequency

    def save_database(self) -> None:
        self.database.to_csv("data.csv", index=False)
        self.database.to_feather("data")


crawler = Crawler(1500)
