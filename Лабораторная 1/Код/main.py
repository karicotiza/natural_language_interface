import pandas as pd

import search

if __name__ == "__main__":
    database = "data.feather"
    search_engine = search.SearchEngine(database)
    while True:
        query = str(input("Query: "))
        search_result = search_engine.search(query)

        if not search_result.empty:
            print(search.make_readable(search_result), "\n\n")
            while True:
                print(
                    f"Pick option:\n"
                    f"0. Enter next query\n"
                    f"1. Title of entry #\n"
                    f"2. Summary of entry #\n"
                    f"3. Get metrics"
                )

                try:
                    picked_option = int(input("Option: "))
                    if picked_option == 0:
                        print("\n")
                        break
                    elif picked_option == 1:
                        number_of_entry = int(input("Number of entry: "))
                        result = search.get_title(search_result, number_of_entry)
                        if result:
                            print(result, "\n\n")
                        else:
                            print("Wrong number\n\n")

                    elif picked_option == 2:
                        number_of_entry = int(input("Number of entry: "))
                        result = search.get_summary(search_result, number_of_entry)
                        if result:
                            print(result, "\n\n")
                        else:
                            print("Wrong number\n\n")
                    elif picked_option == 3:
                        for key, value in search.get_metrics(
                            pd.read_feather(database),
                            search_result
                        ).items():
                            print(f"{key}: {value}")
                        print("\n")
                    else:
                        print("Wrong number\n\n")
                except ValueError:
                    print("Integers only\n\n")
        else:
            print(
                f"No entries\n"
            )
