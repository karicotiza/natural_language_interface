import nltk
import wikipedia
import pandas as pd


class Crawler:
    def __init__(self, attempts):
        self.attempts = attempts
        self.columns = ["Title", "URL", "Summary"]
        self.database = pd.DataFrame(
            columns=self.columns,
        )

        self.crawl()
        self.fix_database()
        self.save_database()

    def crawl(self):
        for page_id in range(self.attempts):
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

    @staticmethod
    def tokenize(sentence):
        valid_parts_of_speech = ["NN", "NNS", "NNP", "NNPS"]

        tokenizer = nltk.TweetTokenizer()
        lemmatizer = nltk.wordnet.WordNetLemmatizer()

        tokenized_sentence = tokenizer.tokenize(sentence)
        tokenized_sentence = [word for word in tokenized_sentence if
                              nltk.pos_tag([word])[0][1] in valid_parts_of_speech]
        tokenized_sentence = [lemmatizer.lemmatize(word).lower() for word in tokenized_sentence]

        frequency = dict(
            (word, tokenized_sentence.count(word)) for word in set(tokenized_sentence)
        )

        return frequency

    def fix_database(self):
        # self.database.drop(["Summary"], axis=1, inplace=True)
        self.database.fillna(0, inplace=True)

    def save_database(self):
        self.database.to_csv("data.csv", index=False)
        self.database.to_feather("data")


crawler = Crawler(40)
