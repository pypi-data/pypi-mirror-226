#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as BS
import html2text as h2t
import hashlib
from .options import get_opts


def mkdir(asOutput: str):
    # TODO make output dir as needed
    pass


def appendUrl(
    asBaseUrl: str,
    alUrls: list[dict[str, str]],
    adUrl: dict[str, str],
):
    try:
        if len(adUrl["href"].split("://")) < 2:
            if adUrl["href"].startswith("/"):
                adUrl["href"] = asBaseUrl.rpartition("/")[0] + adUrl["href"]
            else:
                adUrl["href"] = asBaseUrl.rpartition("/")[0] + "/" + adUrl["href"]
    except KeyError:
        pass
    alUrls.append(adUrl)


def makeSafeFilename(aName: str):
    # Define a set of illegal characters in filenames
    illegalChars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]

    # Replace illegal characters with underscores
    safeName = "".join(["_" if char in illegalChars else char for char in aName])

    return safeName


def writeUrl(
    asUrl: str,
    asOutput: str,
    abCode: bool,
):
    h = h2t.HTML2Text()
    h.mark_code = abCode
    m = hashlib.md5()
    m.update(asUrl.encode("utf-8"))
    hashedUrl = m.hexdigest()
    response = requests.get(asUrl)
    if response.status_code == 200:
        soup = BS(response.content, "html.parser")
        titleTag = soup.find("title")
        title = makeSafeFilename(titleTag.get_text() + "-") if titleTag else ""
        with open(f"{asOutput}/{title}{hashedUrl}.md", "w") as data:
            data.write(h.handle(response.text))


def writeUrls(asUrls: list, asOutput: str, abCode: bool):
    for url in asUrls:
        sUrl = url["href"]
        writeUrl(sUrl, asOutput, abCode)


def getUrls(
    asBaseUrl: str,
    asMatch: str,
) -> list:
    response = requests.get(asBaseUrl)
    soup = BS(response.text, "html.parser")
    urls = []
    for url in soup.findAll("a"):
        if asMatch != "":
            try:
                if asMatch in url["href"]:
                    appendUrl(asBaseUrl, urls, url)
            except KeyError:
                continue
        else:
            appendUrl(asBaseUrl, urls, url)
    return urls


def main():
    args = get_opts()
    # set vars
    bScrapeAll = args.all
    sBaseUrl = args.url
    sMatch = "" if args.match is None else args.match
    sOutput = "." if args.output is None else args.output
    bCode = args.code
    # do da work
    if bScrapeAll:
        urls = getUrls(sBaseUrl, sMatch)
        writeUrls(urls, sOutput, bCode)
    else:
        writeUrl(sBaseUrl, sOutput, bCode)
    return 0


if __name__ == "__main__":
    exit(main())
