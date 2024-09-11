#!./venv/bin python3
""" Docstring to be added once everything is done.
"""

import argparse
import requests
import re
from datetime import datetime
from sys import exit


def download_website(verbose: bool, p_r: int = 0, url: str = "") -> str:
    _response = ""
    _headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/101.0.4951.67 Safari/537.36"
        )
    }
    _url = url
    if p_r == 0:
        _response = requests.get(
            _url,
            "html.parser",
            headers=_headers,
            timeout=10
        )
        print(_response) if verbose else None
        return _response
    elif p_r > 0:
        _url = f"{url} + &r={p_r}"
        _response = requests.get(
            _url,
            "html.parser",
            headers=_headers,
            timeout=10
        )
        return _response


def get_pagestring(verbose: bool, p_code: requests.models.Response) -> None:
    """
    """
    sourcecode = p_code
    for line in sourcecode.iter_lines():
        _strline = line.decode("utf-8")
        v_pagestring = str(
            re.findall(
                r"\<option\ selected=\"selected\"\ value=1\>Page.*", _strline
            )
        )
        if len(v_pagestring) > 2:
            print(v_pagestring) if verbose else None
            return v_pagestring


def extract_pages(verbose: bool, p_code: requests.models.Response) -> list:
    """
    """
    sourcecode = p_code
    sourcecode = re.findall(r"value=(\d+)", sourcecode)
    print(sourcecode) if verbose else None
    return sourcecode


def get_stocks(verbose: bool, p_code: requests.models.Response) -> list:
    """
    """
    sourcecode = p_code
    l_list = []
    for line in sourcecode.iter_lines():
        strline = line.decode("utf-8")
        v_stock = re.findall(r"[A-Z]*\|[0-9]*\.[0-9]*\|[0-9]*", strline)
        if len(v_stock) == 0:
            continue
        l_list.append(v_stock[0].split("|")[0])
    print(l_list) if verbose else None
    return l_list


def main():
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of finviz."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose.",
        default=False
    )
    args = parser.parse_args()

    url: str = args.url
    verbose: bool = args.verbose

    finallist = []

    website_first_load = download_website(verbose, 0, url)
    pagestring = get_pagestring(verbose, website_first_load)
    pagelist = extract_pages(verbose, pagestring)
    for page in pagelist:
        website_iteration = download_website(verbose, int(page), url)
        stocklist = get_stocks(verbose, website_iteration)
        for stock in stocklist:
            finallist.append(stock)
    print(finallist)
    print(f"{len(finallist)} have been found") if verbose else None
    
    finallist = ",".join(finallist)
    with open(
        f"./output-data/stocks-{datetime.now()}.txt", "wt", encoding="utf-8"
    ) as file:
        file.write(finallist)


if __name__ == "__main__":
    main()
else:
    print("No module.")
    exit()
