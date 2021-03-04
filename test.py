from abr.fetcher import Fetcher

if __name__ == "__main__":
    t = Fetcher()
    items = ["97785358970", "Secus Digital", "Woolworths"]
    records = t.parallel_search(items)
    print(records)
