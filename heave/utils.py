"""Utilities functions."""

import os
from pathlib import Path

import pandas as pd


def xlsx_to_csv(file: Path, sheet_name=0) -> Path:
    """Convert xlsx files to csv."""
    new_extension = "csv"
    name, _ = os.path.splitext(os.path.basename(file))
    new_path = os.path.dirname(file)
    new_file = new_path + name + "_" + str(sheet_name) + "." + new_extension
    pd.read_excel(file, sheet_name=sheet_name).to_csv(new_file, index=False)
    return Path(new_file)
