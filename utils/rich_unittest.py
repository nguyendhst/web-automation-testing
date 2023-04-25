import unittest
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.traceback import install


install()


class RichTestResult(unittest.TextTestResult):
    def printErrors(self):
        if self.errors or self.failures:
            console = Console()
            table = Table(title="Test Failures and Errors", style="red")
            table.add_column("Test Case")
            table.add_column("Error")

            for test, err in self.errors + self.failures:
                table.add_row(
                    test.shortDescription() or str(test),
                    Panel(err, title="Exception", expand=False),
                )

            console.print(table)


class RichTestRunner(unittest.TextTestRunner):
    resultclass = RichTestResult
