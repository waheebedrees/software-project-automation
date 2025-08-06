import logging


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.bold_red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%m/%d/%Y %H:%M:%S")
        return formatter.format(record)


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, level=logging.DEBUG):
        super().__init__()
        self.setLevel(level)
        self.setFormatter(CustomFormatter(
            '%(asctime)s - %(levelname)s - %(message)s'))


class CustomFileHandler(logging.FileHandler):
    def __init__(self):
        super().__init__("logfile.log", encoding="UTF-8")
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter(
            "%(message)s",
        ))


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name, level=logging.DEBUG)
        self.propagate = False
        self.addHandler(ConsoleHandler())
        self.addHandler(CustomFileHandler())


def get_logger(name: str) -> Logger:
    """
    Get a custom logger with console and file handlers.
    
    Args:
        name (str): The name of the logger.
    
    Returns:
        Logger: A custom logger instance.
    """
    return Logger(name)
