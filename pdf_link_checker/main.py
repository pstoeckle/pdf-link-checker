"""
Main.
"""
from csv import DictWriter
from dataclasses import asdict
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from re import IGNORECASE, MULTILINE
from re import compile as re_compile
from typing import List, Optional

from PyPDF2 import PdfFileReader
from typer import Argument, Exit, Option, Typer, echo

from pdf_link_checker import __version__
from pdf_link_checker.pdf_link_check import check_pdf_links
from pdf_link_checker.utils import error_echo

_LOGGER = getLogger(__name__)
basicConfig(
    format="%(levelname)s: %(asctime)s: %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=INFO,
    filename="pdf-link-checker.log",
    filemode="w",
)


_REFERENCES = re_compile(r"\n\s*References\s*\n", IGNORECASE | MULTILINE)


def _version_callback(value: bool) -> None:
    if value:
        echo(f"pdf-link-checker {__version__}")
        raise Exit()


app = Typer()


@app.callback()
def _call_back(
    _: bool = Option(
        None,
        "--version",
        is_flag=True,
        callback=_version_callback,
        expose_value=False,
        is_eager=True,
        help="Version",
    )
) -> None:
    """

    :return:
    """


_PDF_FILE_OPTION = Argument(
    None,
    exists=True,
    resolve_path=True,
    dir_okay=False,
    help="The PDF file to check.",
)


@app.command()
def check_links(
    pdf_file: Path = _PDF_FILE_OPTION,
    report_out: Path = Option(
        "report.csv",
        "--report",
        "-r",
        resolve_path=True,
        dir_okay=False,
        help="The CSV file with all the checked links.",
    ),
    ignored_urls: List[str] = Option(
        [],
        "--ignore-url",
        "-I",
        help="URL that should not be checked, e.g., because we now that they are not activated yet.",
    ),
    ci_mode: bool = Option(
        False,
        "--ci",
        "-C",
        is_flag=True,
        help="If set, the command will exit with an error code if there are broken URLs.",
    ),
    csv_delimiter: str = Option(
        ";", "--csv-delimiter", "-c", help="The CSV delimiter, e.g., `;`"
    ),
    ignore_unauthorized: bool = Option(
        False,
        "--ignore-unauthorized",
        "-A",
        is_flag=True,
        help="If this flag is set, we will ignore 403 status codes. "
        "Some websites block scripts, and thus existing links will result in 403 codes.",
    ),
    only_errors: bool = Option(
        False,
        "--only-errors",
        "-O",
        is_flag=True,
        help="If this flag is set, the script will only write non 200 lines in the report.",
    ),
) -> None:
    """
    - Get input PDF and output CSV location.
    - execute check_pdf_links(infilepath, infilepath)
    - Save the report to output CSV location.
    """
    ignored_urls_set = set(u.casefold() for u in ignored_urls)
    echo("Starting")
    link_report = check_pdf_links(pdf_file)

    echo(f"Done: {report_out}")

    with report_out.open("w") as csvout:
        csvwrite = DictWriter(
            csvout,
            delimiter=csv_delimiter,
            fieldnames=["page_no", "url", "code", "request_error"],
        )
        csvwrite.writeheader()
        for r in link_report:
            if only_errors and r.code == 200:
                _LOGGER.info("Skip %s", r)
            else:
                csvwrite.writerow(asdict(r))

    if ci_mode:
        error_entries = [
            line
            for line in link_report
            if not ((line.code == 403 and ignore_unauthorized) or line.code == 200)
        ]
        real_error_entries = [
            line
            for line in error_entries
            if line.url.strip().casefold() not in ignored_urls_set
        ]
        if len(real_error_entries) > 0:
            error_echo(f"We found {len(real_error_entries)} broken URLs.")
            raise Exit(1)


@app.command()
def check_page_limit(
    pdf_file: Path = _PDF_FILE_OPTION,
    limit: int = Option(None, "--page-limit", "-l", help="The maximal number of pages"),
    content_limit: Optional[int] = Option(
        None,
        "--content-limit",
        "-c",
        help="The maximal number of content pages. "
        "If this parameter is passed, we will not only the absolute length of the document but "
        "also the length without references etc.",
    ),
) -> None:
    """
    Check the page limit.
    """
    references_start_at_page: int = -1
    with pdf_file.open("rb") as f:
        readpdf = PdfFileReader(f)
        num_pages = len(readpdf.pages)
        for i, page in enumerate(readpdf.pages):
            text = page.extract_text()
            _LOGGER.debug("On page %d:", i)
            _LOGGER.debug(text)
            if _REFERENCES.search(text) is not None:
                references_start_at_page = i + 1
                break
    _LOGGER.info("%s has %d pages.", pdf_file, num_pages)
    if limit < num_pages:
        error_echo(f"The page limit are {limit} pages, but we have {num_pages}")
        raise Exit(1)

    echo("The PDF is within the page limit.")

    if content_limit is not None:
        if references_start_at_page == -1:
            error_echo("We could not determine where the references start...")
            raise Exit(1)
        if references_start_at_page - 1 <= content_limit:
            echo("The PDF is within the content limit.")
        else:
            error_echo(
                f"The content page limit are {content_limit} pages, but we have {references_start_at_page -1 }"
            )
            raise Exit(1)


if __name__ == "__main__":
    app()
