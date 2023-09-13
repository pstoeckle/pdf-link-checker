"""
TEst.
"""
from pathlib import Path
from unittest import TestCase, main

from typer.testing import CliRunner

from pdf_link_checker.main import app


class PDFTest(TestCase):
    runner: CliRunner

    @classmethod
    def setUpClass(cls) -> None:
        """
        Class.
        """
        cls.runner = CliRunner()

    def test_ci(self) -> None:
        """
        Test.
        """
        result = self.runner.invoke(
            app,
            [
                "check-links",
                str(Path("tests", "data", "pdflink.pdf")),
                "--ci",
            ],
        )
        self.assertEqual(result.exit_code, 1)

    def test_ci_ignore(self) -> None:
        """
        Test.
        """
        result = self.runner.invoke(
            app,
            [
                "check-links",
                str(Path("tests", "data", "pdflink.pdf")),
                "--ci",
                "-I",
                "http://www.adobe.com/suportservice/devrelations/PDFS/TN5150.PDFMARK.PDF",
            ],
        )
        self.assertEqual(0, result.exit_code)


if __name__ == "__main__":
    main()
