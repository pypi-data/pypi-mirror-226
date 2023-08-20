import datetime
import logging
import logging.config
import re
from typing import Annotated, Final

import pandas as pd
import pkg_resources
import typer

from iscwatch.logconfig import logging_config

logging.config.dictConfig(logging_config)

PACKAGE_NAME: Final = "iscwatch"


def cli():
    """CLI entry point executes typer-wrapped main function"""
    typer.run(main)


def main(
    since: Annotated[
        datetime.datetime,
        typer.Option(
            "--since",
            "-s",
            help="Only output those advisories updated or released since specified date.",
            formats=["%Y-%m-%d"],
        ),
    ] = datetime.datetime.min,
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show iscwatch application version and exit."),
    ] = False,
    no_header: Annotated[
        bool,
        typer.Option(
            "--no-header", "-n", help="Omit column header from CSV advisory summary output."
        ),
    ] = False,
    last_updated: Annotated[
        bool,
        typer.Option(
            "--last-updated",
            "-l",
            help="Show date when Intel last updated its security advisories and exit.",
        ),
    ] = False,
):
    """Output security advisory summaries from the Intel Security Center website.

    With no options, iscwatch outputs all Intel security advisory summaries in CSV format with
    column headers.  Typically, a starting date is specified using the --since option to
    constrain the output to a manageable subset.

    """
    if version:
        print_version()
        return

    advisories = advisories_from_html()

    if last_updated:
        print(advisories["Updated"].max().date())
        return

    if since:
        advisories = advisories[advisories["Updated"].between(since, datetime.datetime.now())]

    print(advisories.to_csv(index=False, header=not no_header))


# def print_csv_advisories(advisories: list[Advisory], no_headers: bool):
#     """Convert advisories into dictionaries and output in CSV format."""
#     fieldnames = [field.name for field in fields(Advisory)]
#     # lineterminator argument required to avoid stdout \n\r behavior on windows
#     writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
#     if not no_headers:
#         writer.writeheader()
#     writer.writerows(asdict(advisory) for advisory in advisories)


def print_version():
    """Output current version of the application."""
    try:
        distribution = pkg_resources.get_distribution(PACKAGE_NAME)
        print(f"{distribution.project_name} {distribution.version}")
    except pkg_resources.DistributionNotFound:
        logging.error(f"The package ({PACKAGE_NAME}) is not installed.")


def convert_date(date_string: str) -> datetime.datetime:
    date_pattern = (
        r"(?P<month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\w*"
        r"(\s|&nbsp;)(?P<day>0?[1-9]|[12][0-9]|3[01]), (?P<year>[0-9]{4})"
    )
    if m := re.search(date_pattern, date_string):
        return datetime.datetime.strptime(f"{m['month']} {m['day']}, {m['year']}", "%b %d, %Y")
    return datetime.datetime.min


def make_link(advisory_number: str) -> str:
    base_link = "https://www.intel.com/content/www/us/en/security-center/advisory"
    return f"{base_link}/{advisory_number.lower()}.html"


def advisories_from_html() -> pd.DataFrame:
    advisories = pd.read_html(
        io="https://www.intel.com/content/www/us/en/security-center/default.html",
        converters={"Updated": convert_date, "Release Date": convert_date},  # type: ignore
    )[0]
    advisories["Updated"] = pd.to_datetime(advisories["Updated"])
    advisories["Release Date"] = pd.to_datetime(advisories["Release Date"])
    advisories["Link"] = advisories["Advisory Number"].apply(make_link)

    return advisories
