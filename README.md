# PDF Link Check

[[_TOC_]]


Stituation: You need to upload a PDF somewhere

-  a submission to [EasyChair](https://easychair.org/cfp/)
- a preprint to [arxiv](https://arxiv.org/)
- a slide deck to [moodle](https://www.moodle.tum.de/)

Now, you want to check if all the links are still active and that a the reviewers, reader, or students end up with `404` error codes.
Let this script check that for you!

## Setup

1. Install [Python](https://www.python.org/downloads/)
2. Install the `pdf-link-checker` via the GitLab Python Package Registry.

    ```bash
    pip install pdf-link-checker --extra-index-url https://i4-student:zYyCuhx15tShf5EhRKyo@gitlab.lrz.de/api/v4/projects/102646/packages/pypi/simple
    ```

    **Attention**: On macOS, `pip` is usually the installer of the Python2 instance.
    Please use `pip3` or `pip3.x` in this case.

3. Now you should be able to call `pdf-link-checker` within your shell.

    ```bash
    $ pdf-link-checker --version
    pdf-link-checker 1.1.5
    ```

## Usage

### Check Links

```bash
$ pdf-link-checker check-links --help
Usage: pdf-link-checker check-links [OPTIONS] [PDF_FILE]

  - Get input PDF and output CSV location. - execute
  check_pdf_links(infilepath, infilepath) - Save the report to output CSV
  location.

Arguments:
  [PDF_FILE]  The PDF file to check.

Options:
  -r, --report FILE          The CSV file with all the checked links.
                             [default: report.csv]

  -I, --ignore-url TEXT      URL that should not be checked, e.g., because we
                             now that they are not activated yet.  [default: ]

  -C, --ci                   If set, the command will exit with an error code
                             if there are broken URLs.  [default: False]

  -c, --csv-delimiter TEXT   The CSV delimiter, e.g., `;`  [default: ;]
  -A, --ignore-unauthorized  If this flag is set, we will ignore 403 status
                             codes. Some websites block scripts, and thus
                             existing links will result in 403 codes.
                             [default: False]

  --help                     Show this message and exit.
```

### Check Page Limit

```bash
$ pdf-link-checker check-page-limit --help
Usage: pdf-link-checker check-page-limit [OPTIONS] [PDF_FILE]

  Check the page limit.

Arguments:
  [PDF_FILE]  The PDF file to check.

Options:
  -l, --page-limit INTEGER  The maximal number of pages
  --help                    Show this message and exit.
```

#### Example

```bash
$ pdf-link-checker check-links main.pdf
Starting
100%|█████████| 5/5 [00:30<00:00,  6.18s/it]
Done: .../report.csv
```

## Run Pytest to validate returns

From the script directory, run `pytest` to validate the code. The tests use the PDFs in the **data** folder.

## Contact

If you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@tum.de?subject=GitLab%3A%20PDF-Link-Checker&body=Hi%2C%0AI%20have%20the%20following%20question%20regarding%20the%20pdf-link-checker%20library%3A).
