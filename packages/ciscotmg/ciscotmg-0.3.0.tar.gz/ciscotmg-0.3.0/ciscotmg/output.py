from io import StringIO
import csv
from rich.table import Table
from rich.panel import Panel
from rich.console import Console


class Output:
    """CLI Layout"""

    @staticmethod
    def table(title, columns, rows) -> Table:
        """Table Layout"""
        table = Table(title=title)

        if len(rows) == 0:
            """No results"""
            return Panel(title, expand=False)

        for column in columns:
            table.add_column(column, no_wrap=False)
        for row in rows:
            table.add_row(*row)
        return table

    """CSV Layout"""

    @staticmethod
    def csv(columns, rows):
        output = StringIO()
        csvwriter = csv.writer(output)
        header = columns
        csvwriter.writerow(header)
        for item in rows:
            item_without_newline = [s.replace("\n", "") for s in item]
            csvwriter.writerow(item_without_newline)
        data = output.getvalue()
        output.close()
        return data


def write_to_file(data, filename) -> bool:
    """Write output to file"""
    console = Console(file=filename)
    with console.capture() as capture:
        console.print(data)
    data = capture.get()

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return True
