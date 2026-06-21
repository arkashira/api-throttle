from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Throttle:
    limit: int
    window: timedelta

    def __post_init__(self):
        self.calls = []

    def acquire(self) -> bool:
        now = datetime.now()
        self.calls = [call for call in self.calls if now - call < self.window]
        if len(self.calls) < self.limit:
            self.calls.append(now)
            return True
        return False

    def release(self) -> None:
        if self.calls:
            self.calls.pop(0)
