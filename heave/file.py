"""Extract tabular data into a custom Table object."""

import csv
import os
from pathlib import Path

import openpyxl


class Table:
    """Two-dimensional data with a header."""

    def __init__(self, data: list[tuple[str, ...]]):
        """Initialise table with data."""
        self._data = data

    @property
    def header(self) -> tuple[str, ...]:
        """Return the table header."""
        return self._data[0]

    @property
    def rows(self):
        """Yield the table rows."""
        yield from self._data[1:]

    def __eq__(self, other):
        """Return True if the data is equal."""
        return self._data == other._data


def read_csv(file: Path) -> Table:
    """Read a csv file and return a Table."""
    if file.suffix == ".xlsx":
        file = xlsx_to_csv(file)
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]
    return Table(data)


def write_csv(data: Table, file: Path) -> None:
    """Write a Table to a csv file."""
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        rows = [data.header, *data.rows]
        writer.writerows(rows)


def xlsx_to_csv(file: Path, sheet_name="Sheet1") -> Path:
    """Convert xlsx file to csv."""
    # Create new file name
    new_extension = "csv"
    name, _ = os.path.splitext(os.path.basename(file))
    new_path = os.path.dirname(file)
    new_file = os.path.join(new_path, f"{name}_{sheet_name}.{new_extension}")

    # Open the Excel file
    workbook = openpyxl.load_workbook(filename=file)
    worksheet = workbook[sheet_name]

    # Open the CSV file
    with open(new_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the Excel rows and write to CSV
        for row in worksheet.rows:
            row_data = []
            for cell in row:
                row_data.append(cell.value if cell else "")
            writer.writerow(row_data)

    return Path(new_file)
