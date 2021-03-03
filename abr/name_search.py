from typing import Tuple
import urllib.request as request
from urllib.error import URLError
from bs4 import BeautifulSoup


def name_search(name, api_token) -> Tuple[str, str]:
    """Returns a tuple of name (as provided) plus the closest matching ABN from the ABR Registry meeting the [95] threshold"""

    req = request.Request(query_url(name, api_token))
    try:
        with request.urlopen(req) as res:
            data = res.read()
            return name, parse_response(data)
    except URLError as e:
        print(e)
        return (name, "")


def query_url(name, api_token):
    host = "https://abr.business.gov.au"
    prefix = "/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByNameSimpleProtocol?"
    params = {
        "name": str(name).replace(" ", "%20").replace("&", "%26").replace("'", "%27"),
        "postcode": "",
        "legalName": "",
        "tradingName": "N",
        "businessName": "",
        "activeABNsOnly": "Y",
        "NSW": "",
        "SA": "",
        "ACT": "",
        "VIC": "",
        "WA": "",
        "NT": "",
        "QLD": "",
        "TAS": "",
        "authenticationGuid": api_token,
        "maxSearchResults": "",
        "minimumScore": 95,
    }

    return host + prefix + "&".join(f"{str(k)}={params[k]}" for k in params)


def parse_response(res) -> str:
    """Take the ABR Query Response and return the ABN as a string"""

    try:
        soup = BeautifulSoup(res, "lxml")
    except TypeError:
        return ""

    search_results = soup.find_all("searchresultsrecord")
    if not search_results:
        return ""

    abns = dict()
    for record in search_results:
        score = int(record.find("score").text.strip())
        if score < 90:
            continue
        abn = record.find("abn").find("identifiervalue").text.strip()
        abns[abn] = score

    try:
        if sorted_abns := sorted(abns.items(), key=lambda x: x[1], reverse=True):
            return sorted_abns[0][0]
        else:
            return ""
    except IndexError:
        return ""
