"""Tests for the extract module."""
import os
from pathlib import Path

import pandas as pd
import pytest

from heave import file, utils
from heave.file import Table


class TestTable:
    """Test the Table class."""

    def test_init(self):
        """Test initialisation of the Table class."""
        data = [("header1", "header2"), ("data1", "data2")]
        table = Table(data)
        assert table.header == ("header1", "header2")
        assert list(table.rows) == [("data1", "data2")]


class TestCsv:
    """Test the read_csv function."""

    test_file = Path("temp.csv")

    @pytest.fixture(autouse=True)
    def temp_file(self):
        """Create a temporary csv file."""
        with open(self.test_file, "w") as f:
            f.write("header1,header2\n")
            f.write("data1,data2\n")
        yield
        os.remove(self.test_file)

    def test_read_csv(self):
        """Test reading a csv file."""
        table = file.read_csv(self.test_file)
        assert table.header == ("header1", "header2")
        assert list(table.rows) == [("data1", "data2")]

    def test_write_csv(self):
        """Test writing a csv file."""
        data = Table([("header3", "header4"), ("data3", "data4")])
        file.write_csv(data, self.test_file)
        table = file.read_csv(self.test_file)
        assert table == data


class TestXlsx:
    """Test xlsx to csv conversion."""

    test_file = Path("temp1.xlsx")

    @pytest.fixture(autouse=True)
    def temp_file(self):
        """Create a temporary xlsx file and yield its directory."""
        with open(self.test_file, "wb") as f:
            # ... your data creation logic ...
            data1 = {"header1": ["data1"], "header2": ["data2"]}
            data2 = {
                "heading1": ["data1"],
                "heading2": ["data2"],
                "heading3": ["data3"],
            }
            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)

            writer = pd.ExcelWriter(f, engine="xlsxwriter")
            df1.to_excel(writer, sheet_name="1", index=False)
            df2.to_excel(writer, sheet_name="2", index=False)
            writer._save()
        yield
        os.remove(self.test_file)

    def test_xlsx_to_csv(self):
        """Test converting xlsx to csv using xlsx_to_csv function."""
        # first sheet and its content
        csv_file1 = utils.xlsx_to_csv(self.test_file, sheet_name=0)
        assert csv_file1.exists()
        converted_data = pd.read_csv(csv_file1)
        assert len(converted_data.columns) == 2
        assert converted_data["header1"].tolist() == ["data1"] and converted_data[
            "header2"
        ].tolist() == ["data2"]
        # second sheet and its content
        csv_file2 = utils.xlsx_to_csv(self.test_file, sheet_name=1)
        assert csv_file2.exists()
        converted_data = pd.read_csv(csv_file2)
        assert len(converted_data.columns) == 3
        assert (
            converted_data["heading1"].tolist() == ["data1"]
            and converted_data["heading2"].tolist() == ["data2"]
            and converted_data["heading3"].tolist() == ["data3"]
        )
        os.remove(csv_file1)
        os.remove(csv_file2)
