import pandas as pd
import math


class SearchEngine:
    def __init__(self, database: str) -> None:
        self.database = pd.read_feather(database)
        self.number_of_records = len(self.database)
        self.average_record_length = self.calculate_average_record_length()

    def calculate_average_record_length(self) -> float:
        length = 0
        for summary in self.database["Summary"]:
            length += len(summary.split())
        return float(length / self.number_of_records)

    def search(self, query: str, amount_of_results: int) -> pd.DataFrame:
        query = query.lower()
        scores = pd.DataFrame()
        if self.database.get([query][0], None) is not None:
            contains = len(self.database[self.database[query] >= 1])
            k1 = 2.0
            b = 0.75
            idf = math.log(
                (self.number_of_records - contains + 0.5) /
                (contains + 0.5)
            )

            for record in range(self.number_of_records):
                score = idf * (
                        (self.database[query].iat[record] * (k1 + 1)) /
                        (self.database[query].iat[record] + k1 * (
                                1 - b + b * len(self.database["Summary"].iat[0].split()) / self.average_record_length)
                         )
                )
                data = pd.DataFrame(
                    columns=["Title", "URL", "Summary", "Score"],
                    data=[[
                        self.database["Title"].iat[record],
                        self.database["URL"].iat[record],
                        self.database["Summary"].iat[record],
                        score
                    ]]
                )
                scores = pd.concat([scores, data], axis=0, ignore_index=True)

            return self.trim(scores, amount_of_results)

        else:
            return pd.DataFrame(
                columns=["Title", "URL", "Summary", "Score"],
                data=[[None, None, None, None]]
            )

    @staticmethod
    def trim(results: pd.DataFrame, amount_of_results: int) -> pd.DataFrame:
        return results.sort_values("Score", ascending=False).head(amount_of_results)


search_engine = SearchEngine("data")
print(search_engine.search("Microsoft", 10))
