"""Utilities functions."""

import csv
import os
from pathlib import Path

import openpyxl


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
