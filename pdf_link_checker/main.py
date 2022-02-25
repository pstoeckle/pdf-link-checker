"""
Main.
"""
from csv import DictWriter
from dataclasses import asdict
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import List

from pdf_link_checker import __version__
from pdf_link_checker.pdf_link_check import check_pdf_links
from pdf_link_checker.utils import error_echo
from typer import Exit, Option, Typer, echo

_LOGGER = getLogger(__name__)
basicConfig(
    format="%(levelname)s: %(asctime)s: %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=INFO,
    filename="pdf-link-checker.log",
    filemode="w",
)


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


@app.command()
def check_links(
    pdf_file: Path = Option(
        None,
        "--pdf-file",
        "-p",
        exists=True,
        resolve_path=True,
        dir_okay=False,
        help="The PDF file to check.",
    ),
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
            csvwrite.writerow(asdict(r))

    if ci_mode:
        error_entries = [line for line in link_report if line.code != 200]
        real_error_entries = [
            line
            for line in error_entries
            if line.url.strip().casefold() not in ignored_urls_set
        ]
        if len(real_error_entries) > 0:
            error_echo(f"We found {len(real_error_entries)} broken URLs.")
            raise Exit(1)


if __name__ == "__main__":
    app()
