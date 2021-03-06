# About

This lib is designed to help find ABNs for companies in Australia. It can perform searches on both Name and ABN, and will return an ABR Record for the best match.

# Usage

The base class is the fetcher, which is imported from fetcher.py.

Basic usage is the following:

```python
from abr import fetcher

f = Fetcher()
items_to_search_for = ["97785358970", "Secus Digital"]
for item in items_to_search_for:
    f.search(item)
```

If you need to find many ABNs at a time, you can perform searches in parallel:

```python
from abr import fetcher

f = Fetcher()
items_to_search_for = ["97785358970", "Secus Digital"]
f.parallel_search(items)
```

# Example ABR Record

An ABR Record looks like the following:

```python
class AbrRecord(NamedTuple):
    abn: str
    name: str
    is_active: bool
    trading_name: str
    entity_type: str
    address_state: str
    address_postcode: str
    is_acnc_registered: bool
    charity_type: str
    tax_concessions: List[str]
    is_gst_registered: bool
```
