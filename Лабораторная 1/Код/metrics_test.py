import pandas as pd
from pprint import pprint

import search

requests = [
    "Anarchism in Alabama",
    "Popular music group from Sweden",
    "Mountain in Europe",
    "What is Albedo?",
    "President of the united states",
]

search_engine = search.SearchEngine("data.feather")
for request in requests:
    search_result = search_engine.search(request)

    pprint(
        search.get_metrics(
            pd.read_feather("data.feather"),
            search_result,
        )
    )
