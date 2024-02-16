"""Extract tabular data into a custom Table object."""
import csv


class Table:
    """Two-dimensional data with a header."""

    def __init__(self, data: list[list[str]]):
        """Initialise table with data."""
        self._data = data

    @property
    def header(self):
        """Return the table header."""
        return self._data[0]

    @property
    def rows(self):
        """Yield the table rows."""
        for row in self._data[1:]:
            yield row


def read_csv(file: str) -> Table:
    """Read a csv file and return a Table."""
    with open(file, "r") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return Table(data)
