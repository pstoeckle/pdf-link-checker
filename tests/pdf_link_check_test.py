"""Tests for pdf_linker.check.py"""
from pathlib import Path
from unittest import main

import pdf_link_checker.pdf_link_check as plc
from pdf_link_checker.record import Record


def test_get_split_large():
    """Function to split a number into four equal(ish) sections."""
    number_to_split = 100
    split = plc.get_split(number_to_split)

    assert [(0, 25), (26, 50), (51, 75), (76, 100)] == split


def test_get_split_small():
    """Function to split a number into four equal(ish) sections."""
    number_to_split = 10
    try:
        _ = plc.get_split(number_to_split)
        out_stuff = "Success"
    except Exception as e:
        out_stuff = str(e)

    assert "Number too small to split into four sections." == out_stuff


def test_check_pdf_links_long():
    """Function to test crawl for a long PDF (under 13 pages)"""
    file_check = plc.check_pdf_links(Path("tests", "data", "testpdf.pdf"))
    data_check = Record(
        page_no=3,
        url="https://en.wikipedia.org/wiki/Fish",
        code=200,
        request_error="NA",
    )

    assert data_check == file_check[0]


def test_check_pdf_links_short():
    """Function to test crawl for a short PDF (under 13 pages)"""
    file_check = plc.check_pdf_links(Path("tests", "data", "pdflink.pdf"))
    data_check = Record(
        page_no=1,
        url=" http://www.adobe.com/suportservice/devrelations/PDFS/TN5150.PDFMARK.PDF",
        code=404,
        request_error="NA",
    )

    assert data_check == file_check[0]


if __name__ == "__main__":
    main()
