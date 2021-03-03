from typing import NamedTuple, List


class AbrRecord(NamedTuple):
    abn: str
    name: str
    is_active: bool
    trading_name: str
    entity_type: str
    address_state: str
    address_postcode: str

    # If Charity
    is_acnc_registered: bool
    charity_type: str
    tax_concessions: List[str]

    # If not charity
    is_gst_registered: bool
