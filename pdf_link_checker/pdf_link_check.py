""" PDF Link Check
    For more information see: https://github.com/mattbriggs/pdf-link-checker
    PDFLinkCheck.py checks the hyperlinks in an Portable Document Format (PDF)
    file.

    Release V1.1.1 2020.1.23
"""
from logging import getLogger
from operator import itemgetter
from pathlib import Path
from threading import Thread
from typing import Any, MutableMapping, Sequence, Tuple, MutableSet

from requests import get

from pdf_link_checker.utils import error_echo
from PyPDF2 import PdfFileReader
from tqdm import tqdm
_LOGGER = getLogger(__name__)

def get_split(numtosplit):
    """Split a number into four equal(ish) sections. Number of pages must be greater
    than 13."""
    if numtosplit > 13:
        sections = []
        breaksize = int(numtosplit / 4)
        sec1_start = 0
        sec1_end = breaksize
        sec2_start = breaksize + 1
        sec2_end = breaksize * 2
        sec3_start = sec2_end + 1
        sec3_end = breaksize * 3
        sec4_start = sec3_end + 1
        sec4_end = numtosplit

        sections = [
            (sec1_start, sec1_end),
            (sec2_start, sec2_end),
            (sec3_start, sec3_end),
            (sec4_start, sec4_end),
        ]

        return sections

    raise ValueError("Number too small to split into four sections.")


def get_links_from_page(indexstart, indexend, reportlist, pdf):
    """- Extract pages from the PDF using the incoming range.
    - For each page, find annotations, and URIs in the annotations.
        - Get the URIs.
            - For each URI try to make a web request and get the response code.
            - Record the page number, URI, and response code result or NA for
              timeouts.
    """
    checked_urls: MutableSet[str] = set()

    for i in tqdm(range(indexstart, indexend)):
        page_obj = pdf.getPage(i)
        page_no = i + 1
        try:
            annots = page_obj["/Annots"]
            for a in annots:
                u = a.getObject()
                if "/A" in u:
                    uris = u["/A"]
                    if "/URI" in uris:
                        raw_url: str = uris["/URI"]
                        if raw_url.strip().casefold().startswith("mailto:"):
                            _LOGGER.info(f"Ignoring email address {raw_url}")
                            continue
                        if raw_url.strip().casefold() in checked_urls:
                            _LOGGER.info(f"We already checked {raw_url}")
                            continue
                        try:
                            x = get(raw_url, timeout=5, stream=True)
                            code = x.status_code
                            x.close()
                            request_error = "NA"
                        except Exception as e:
                            error_echo(str(e))
                            code = "NA"
                            request_error = str(e)
                        _LOGGER.info(f"{page_no} : {raw_url} : {code}")
                        record = [page_no, raw_url, code, request_error]
                        checked_urls.add(raw_url.strip().casefold())
                        reportlist.append(record)
        except KeyError:
            _LOGGER.info(f"no annotations on page {page_no}")
    return reportlist


def check_pdf_links(infilepath: Path) -> Sequence[Any]:
    """- Get the number of pages, and split into four equal sections
     - Get the range for each section, and send each section range to the parser
    running its own thread.
     - return a list of lists [[]] with report data."""
    pdf = PdfFileReader(str(infilepath))
    pages = pdf.numPages
    link_report = []
    if pages < 13:
        get_links_from_page(0, pages, link_report, pdf)
    else:
        split = get_split(pages)
        threads = []
        for i in range(4):
            th = Thread(
                target=get_links_from_page,
                args=(split[i][0], split[i][1], link_report, pdf),
            )
            th.start()
            threads.append(th)
        [th.join() for th in threads]
    link_report.sort(key=itemgetter(0))
    link_report.insert(0, ["page", "uri", "status", "request-error"])
    return link_report
