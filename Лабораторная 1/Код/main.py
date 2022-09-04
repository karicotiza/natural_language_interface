import search

if __name__ == "__main__":
    search_engine = search.SearchEngine("data.feather")
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
                )

                try:
                    picked_option = int(input("Option: "))
                    if picked_option == 0:
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
                    else:
                        print("Wrong number\n\n")
                except ValueError:
                    print("Integers only\n\n")
        else:
            print(
                f"No entries\n"
            )
