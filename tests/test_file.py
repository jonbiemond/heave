"""Tests for the extract module."""
import os

import pytest

from heave.file import Table, read_csv


class TestTable:
    """Test the Table class."""

    def test_init(self):
        """Test initialisation of the Table class."""
        data = [["header1", "header2"], ["data1", "data2"]]
        table = Table(data)
        assert table.header == ["header1", "header2"]
        assert [row for row in table.rows] == [["data1", "data2"]]


class TestCsv:
    """Test the read_csv function."""

    test_file = "temp.csv"

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
        table = read_csv(self.test_file)
        assert table.header == ("header1", "header2")
        assert [row for row in table.rows] == [("data1", "data2")]
