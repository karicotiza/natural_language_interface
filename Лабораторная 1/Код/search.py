import math
import pandas as pd
import preprocessing


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

    def search(self, query: str) -> pd.DataFrame:
        query = preprocessing.normalize(query)

        results = self.database[["Title", "URL", "Summary"]].copy()

        for word in query:
            if word in self.database.columns[2:]:
                column = pd.DataFrame()
                contains = len(self.database[self.database[word] >= 1])
                k1 = 2.0
                b = 0.75
                idf = math.log(
                    (self.number_of_records - contains + 0.5) /
                    (contains + 0.5)
                )

                for record in range(self.number_of_records):
                    score = idf * (
                            (self.database[word].iat[record] * (k1 + 1)) /
                            (self.database[word].iat[record] + k1 * (1 - b + b * len(
                                self.database["Summary"].iat[0].split()) / self.average_record_length)
                             )
                    )
                    column = pd.concat([column, pd.DataFrame([score])], axis=0, ignore_index=True)

                results[word] = column

        results["Overall Score"] = results.sum(numeric_only=True, axis=1)

        return self.trim(results)

    @staticmethod
    def trim(results: pd.DataFrame) -> pd.DataFrame:
        return results[results["Overall Score"] > 0].sort_values("Overall Score", ascending=False, ignore_index=True)


def make_readable(results: pd.DataFrame) -> pd.DataFrame or None:
    if not results.empty:
        table_of_content = pd.DataFrame(
            columns=["URL", "Keywords"]
        )

        for index, row, in results.iterrows():
            url = row["URL"]
            clean_row = row.to_frame().transpose()
            clean_row = clean_row.replace(0, None).dropna(axis=1, how="all")
            keywords = list(clean_row.columns[3:-1])

            data = pd.DataFrame(
                columns=table_of_content.columns,
                data=[[url, keywords]]
            )
            table_of_content = pd.concat([table_of_content, data], axis=0, ignore_index=True)

        return table_of_content


def get_title(results: pd.DataFrame, index) -> str:
    return results["Title"].iloc[index]


def get_url(results: pd.DataFrame, index) -> str:
    return results["URL"].iloc[index]


def get_summary(results: pd.DataFrame, index) -> str:
    return results["Summary"].iloc[index]


search_engine = SearchEngine("data.feather")
search_result = search_engine.search("united states")

# print(search_result)
print(make_readable(search_result))

# for column in search_result.columns:
#     print(search_result[column])
