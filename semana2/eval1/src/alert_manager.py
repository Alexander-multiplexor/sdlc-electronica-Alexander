from abc import ABC, abstractmethod
from pathlib import Path


class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class ConsoleAlertStrategy(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[CONSOLE ALERT] {message}")

class FileAlertStrategy(AlertStrategy):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def send(self, message: str) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")

class AlertManager:
    def __init__(self) -> None:
        self._strategies: list[AlertStrategy] = []

    def add_strategy(self, strategy: AlertStrategy) -> None:
        self._strategies.append(strategy)

    def notify(self, message: str) -> None:
        for strategy in self._strategies:
            strategy.send(message)