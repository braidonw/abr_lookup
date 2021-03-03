from typing import Tuple, Optional
import urllib.request as request
from urllib.error import URLError
from bs4 import BeautifulSoup
from .abr_record import AbrRecord


def abn_search(abn: str, api_token: str) -> AbrRecord:
    """Returns an ABR Record object for each ABN Provided"""

    req = request.Request(query_url(abn, api_token))
    try:
        with request.urlopen(req) as res:
            data = res.read()
            return parse_response(data)
    except URLError as e:
        print(e)
        return None


def query_url(abn: str, api_token: str):
    host = "https://abr.business.gov.au"
    prefix = f"/abrxmlsearch/AbrXmlSearch.asmx/SearchByABNv202001?searchString={abn}&includeHistoricalDetails=N&authenticationGuid={api_token}"
    return host + prefix


def parse_response(data: str) -> Optional[AbrRecord]:
    """Parse ABR response and return ABR Record object"""

    try:
        soup = BeautifulSoup(data, "lxml")
    except TypeError:
        return None
    results = soup.find("businessentity202001")

    if abn_section := results.find("abn"):
        abn = abn_section.find("identifiervalue").text
    else:
        abn = ""

    if status_section := results.find("entitystatus"):
        is_active = status_section.find("entitystatuscode").text == "Active"
    else:
        is_active = False

    if mainname_section := results.find("mainname"):
        name = mainname_section.find("organisationname").text
    else:
        name = ""

    if maintradingname_section := results.find("maintradingname"):
        trading_name = maintradingname_section.find("organisationname").text
    else:
        trading_name = ""

    if entitytype_section := results.find("entitytype"):
        entity_type = entitytype_section.find("entitydescription").text
    else:
        entity_type = None

    if address_section := results.find("mainbusinessphysicaladdress"):
        address_state = address_section.find("statecode").text
        address_postcode = address_section.find("postcode").text
    else:
        address_state = ""
        address_postcode = ""

    if acnc_section := results.find("acncregistration"):
        is_acnc_registered = acnc_section.find("status").text == "Registered"
    else:
        is_acnc_registered = False

    if charity_section := results.find("charitytype"):
        charity_type = charity_section.find("charitytypedescription").text
    else:
        charity_type = ""

    tax_concessions = []
    for section in results.find_all("taxconcessioncharityendorsement"):
        tax_concessions.append(section.find("endorsementtype").text)

    is_gst_registered = results.find("goodsandservicestax") != None

    return AbrRecord(
        abn=abn,
        name=name,
        is_active=is_active or False,
        trading_name=trading_name or None,
        entity_type=entity_type or None,
        address_state=address_state,
        address_postcode=address_postcode,
        is_acnc_registered=is_acnc_registered or False,
        charity_type=charity_type or None,
        tax_concessions=tax_concessions or [],
        is_gst_registered=is_gst_registered or False,
    )
