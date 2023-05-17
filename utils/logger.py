from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
import logging
from rich.logging import RichHandler


#logging.basicConfig(
#    level="NOTSET",
#    format="%(message)s",
#    datefmt="[%X]",
#    handlers=[RichHandler(rich_tracebacks=True)]
#)

class Logger:
    def __init__(self, level="NOTSET"):
        self.console = Console()
        self.logger = logging.getLogger("rich")

        logging.basicConfig(
            level=level,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True)],
        )
        install()


    def log(self, message, level):
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "critical":
            self.logger.critical(message)
        elif level == "debug":
            self.logger.debug(message)
        elif level == "trace":
            self.logger.trace(message)

    def log_panel(self, message, level):
        if level == "info":
            self.logger.info(Panel(message))
        elif level == "warning":
            self.logger.warning(Panel(message))
        elif level == "error":
            self.logger.error(Panel(message))
        elif level == "critical":
            self.logger.critical(Panel(message))
        elif level == "debug":
            self.logger.debug(Panel(message))
        elif level == "trace":
            self.logger.trace(Panel(message))

    def log_exception(self, message, level):
        if level == "info":
            self.logger.info(Panel(message, title="Exception", expand=False))
        elif level == "warning":
            self.logger.warning(Panel(message, title="Exception", expand=False))
        elif level == "error":
            self.logger.error(Panel(message, title="Exception", expand=False))
        elif level == "critical":
            self.logger.critical(Panel(message, title="Exception", expand=False))
        elif level == "debug":
            self.logger.debug(Panel(message, title="Exception", expand=False))
        elif level == "trace":
            self.logger.trace(Panel(message, title="Exception", expand=False))

    def log_traceback(self, message, level):
        if level == "info":
            self.logger.info(Panel(message, title="Traceback", expand=False))
        elif level == "warning":
            self.logger.warning(Panel(message, title="Traceback", expand=False))
        elif level == "error":
            self.logger.error(Panel(message, title="Traceback", expand=False))
        elif level == "critical":
            self.logger.critical(Panel(message, title="Traceback", expand=False))
        elif level == "debug":
            self.logger.debug(Panel(message, title="Traceback", expand=False))
        elif level == "trace":
            self.logger.trace(Panel(message, title="Traceback", expand=False))