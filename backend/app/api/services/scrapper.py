from urllib import request
from functools import reduce
from datetime import datetime
from functools import partial
import re


from bs4 import BeautifulSoup
from fastapi import Depends
import pytz


from backend.app.setup.logging import logger
from backend.app.api.models.base import BaseModel
from backend.app.api.utils.misc import convert_to_bytes
from backend.app.api.constants import UNIT_MULTIPLIER

BASE_URL = "http://200.152.38.155/CNPJ/dados_abertos_cnpj"


class FileInfo(BaseModel):
    """
    Pydantic model representing a CNPJ file.

    Attributes:
        filename (str): The name of the CNPJ file.
        updated_at (datetime): The date and time when the CNPJ file was last updated.
    """

    filename: str
    updated_at: datetime
    file_size_bytes: int = 0

    def __dict__(self):
        return {
            "filename": self.filename,
            "updated_at": self.updated_at,
            "file_size_bytes": self.file_size_bytes,
        }

# Define helper functions


def or_map(a, b):
    return a or b


def is_size_type(text, size_types):
    return reduce(or_map, [text.endswith(size_type)
                  for size_type in size_types])


def collect_date(text, pattern):
    return text and re.search(pattern, text)


# Partially apply functions
regex_pattern = r"\d{4}-\d{2}-\d{2}"
size_types = UNIT_MULTIPLIER.keys()
TIMEZONE_SAO_PAULO = pytz.timezone("America/Sao_Paulo")

collect_date_partial = partial(collect_date, pattern=regex_pattern)
is_size_type_partial = partial(is_size_type, size_types=size_types)
or_map_partial = partial(or_map)


class CNPJScrapService:
    def __init__(self) -> None:
        self.base_url = BASE_URL

    def get_previous_year_month(self, year_month_str):
        """
        Returns the previous year-month string.

        Args:
            year_month_str (str): The current year-month string in the format 'YYYY-MM'.

        Returns:
            str: The previous year-month string.
        """
        year, month = map(int, year_month_str.split("-"))
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        return f"{year:04d}-{month:02d}"

    def scrap_files_date(self):
        """
        Scrapes the RF (Receita Federal) website to extract file information.

        Returns:
            list: A list of tuples containing the updated date and filename of the files
            found on the RF website.
        """
        current_year_month = datetime.now().strftime("%Y-%m")
        year_month = self.get_previous_year_month(current_year_month)
        data_url = f"{self.base_url}/{year_month}/"

        raw_html = request.urlopen(data_url)
        raw_html = raw_html.read()

        # Formatar página e converter em string
        page_items = BeautifulSoup(raw_html, "lxml")

        # Find all table rows
        table_rows = page_items.find_all("tr")

        # Extract data from each row
        files_info = {}
        for row in table_rows:
            # Find cells containing filename (anchor tag) and date
            filename_cell = row.find("a")

            date_cell = row.find("td", text=collect_date_partial)

            def or_map(a, b):
                return a or b

            def is_size_map(text):
                return text and is_size_type_partial(text)

            size_cell = row.find("td", text=is_size_map)

            has_data = filename_cell and date_cell and size_cell
            if has_data:
                filename = filename_cell.text.strip()

                if filename.endswith(".zip"):
                    # Extract date and format it
                    date_text = date_cell.text.strip()

                    # Try converting date text to datetime object (adjust
                    # format if needed)
                    try:
                        updated_at = datetime.strptime(
                            date_text, "%Y-%m-%d %H:%M")
                        updated_at = TIMEZONE_SAO_PAULO.localize(updated_at)
                        updated_at = updated_at.replace(
                            hour=0, minute=0, second=0, microsecond=0)

                    except ValueError:
                        # Handle cases where date format doesn't match
                        logger.error(
                            f"Error parsing date for file: {filename}")

                    size_value_str = size_cell.text.strip()

                    file_info = FileInfo(
                        filename=filename,
                        updated_at=updated_at,
                        file_size_bytes=convert_to_bytes(size_value_str),
                    )
                    files_info[filename] = dict(file_info)

        return files_info

    def max_update_at(self):
        """
        Scrapes the RF (Receita Federal) website to extract the most recent file's date.

        Returns:
            datetime: The date and time when the most recent file was last updated.
        """

        files_info = self.scrap_files_date()
        max_date = max(
            files_info.values(),
            key=lambda x: x["updated_at"])["updated_at"]
        return max_date


def get_cnpj_scrap_service():
    return CNPJScrapService()


CNPJScrapServiceDependency = Depends(get_cnpj_scrap_service)
