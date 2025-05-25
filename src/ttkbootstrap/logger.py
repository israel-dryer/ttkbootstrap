from enum import Enum
from datetime import datetime


class LogLevel(Enum):
    INFO = ("ℹ️", "INFO")
    WARNING = ("⚠️", "WARNING")
    ERROR = ("❌", "ERROR")
    SUCCESS = ("✅", "SUCCESS")
    DEBUG = ("🐞", "DEBUG")

    def __init__(self, icon, label):
        self.icon = icon
        self.label = label


class Logger:
    def __init__(self, enable_timestamp: bool = True, enabled: bool = True):
        self.enable_timestamp = enable_timestamp
        self.enabled = enabled

    def log(self, title: str, description: str, level: LogLevel = LogLevel.INFO):
        if not self.enabled: return
        timestamp = f"{datetime.now():%Y-%m-%d %H:%M:%S} " if self.enable_timestamp else ""
        print(f"{timestamp}{level.value[0]} [{title}] {description}")

    def info(self, title, description): self.log(title, description, LogLevel.INFO)

    def warning(self, title, description): self.log(title, description, LogLevel.WARNING)

    def error(self, title, description): self.log(title, description, LogLevel.ERROR)

    def success(self, title, description): self.log(title, description, LogLevel.SUCCESS)

    def debug(self, title, description): self.log(title, description, LogLevel.DEBUG)


logger = Logger(False)