import json
import os

import pandas as pd


class SearchEngine:
    CHUNK_SIZE = 1000  # prevent memory issue

    def __init__(self, source_path: str):
        os.path.dirname(__file__)
        self.source = os.path.join(os.path.dirname(__file__), source_path)

    def chunk_from_reader_to_json(self, reader, per_page: int, page: int, filter_text: str = None):
        position = 0
        count = 0
        res = list()
        has_more = False

        for chunk in reader:

            if filter_text is not None:
                chunk = self.filter_df(chunk, filter_text)

            for index, row in chunk.iterrows():
                if count == per_page:
                    has_more = True
                    break

                if position >= (page - 1) * per_page:
                    res.append(json.loads(row.to_json()))
                    count += 1

                position += 1

        return res, has_more

    def get_all(self, per_page: int, page: int):
        temp = pd.read_csv(self.source, iterator=True, chunksize=self.CHUNK_SIZE)

        return self.chunk_from_reader_to_json(temp, per_page=per_page, page=page)

    def search(self, text: str, per_page: int, page: int):
        temp = pd.read_csv(self.source, iterator=True, chunksize=self.CHUNK_SIZE)

        return self.chunk_from_reader_to_json(temp, per_page=per_page, page=page, filter_text=text)

    @staticmethod
    def filter_df(df, search_string):
        filter_condition = df.applymap(lambda cell: isinstance(cell, str) and search_string in cell)
        filtered_df = df[filter_condition.any(axis=1)]
        return filtered_df
