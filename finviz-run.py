#!./venv/bin python3
""" Docstring to be added once everything is done.
"""

import argparse
import requests
import re
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
    """get_pages - Extract the page string where the number
    of the pages can be found.

    :param p_code: Website source code
    :type p_code: requests.models.Response
    :return: String containing the page numbers
    :rtype: str
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

    # finallist = []

    website_first_load = download_website(verbose, 0, url)

    pagestring = get_pagestring(verbose, website_first_load)


if __name__ == "__main__":
    main()
else:
    print("No module.")
    exit()
