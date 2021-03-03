from typing import List
import os
from dotenv import load_dotenv
from .name_search import name_search
from .abn_search import abn_search
from .abr_record import AbrRecord
from .validate_abn import validate_abn
from .parallel_lookup import parallel_lookup


class Fetcher:

    API_TOKEN: str

    def __init__(self):
        # Update params to include the access GUID for ABR
        load_dotenv()
        self.API_TOKEN = os.getenv("ABR_GUID") or ""
        print(f"Using API Token: {self.API_TOKEN}")

    def search(self, term):
        if validate_abn(term):
            return self.abn_search(term)
        abn = self.name_search(term)[1]
        return self.abn_search(abn)

    def name_search(self, name):
        return name_search(name, self.API_TOKEN)

    def abn_search(self, abn):
        return abn_search(abn, self.API_TOKEN)

    def parallel_search(self, items):
        return parallel_lookup(items, self.search)