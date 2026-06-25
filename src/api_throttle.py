import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class StatusCode(Enum):
    SUCCESS = 200
    TOO_MANY_REQUESTS = 429

@dataclass
class Response:
    status_code: int

class ApiThrottle:
    def __init__(self, max_backoff: int = 60, max_retries: int = 5):
        self.max_backoff = max_backoff
        self.max_retries = max_retries
        self.retry_count = 0
        self.backoff_interval = 1

    def exponential_backoff(self) -> None:
        jitter = random.uniform(-0.1, 0.1)
        backoff_interval_with_jitter = self.backoff_interval * (1 + jitter)
        time.sleep(backoff_interval_with_jitter)
        self.backoff_interval = min(self.backoff_interval * 2, self.max_backoff)

    def retry(self, response: Response) -> Optional[Response]:
        if response.status_code == StatusCode.TOO_MANY_REQUESTS.value:
            if self.retry_count < self.max_retries:
                self.exponential_backoff()
                self.retry_count += 1
                # Simulate a new request
                return Response(StatusCode.TOO_MANY_REQUESTS.value)
            else:
                return None
        else:
            self.retry_count = 0
            self.backoff_interval = 1
            return response

    def make_request(self) -> Response:
        # Simulate a request
        return Response(StatusCode.TOO_MANY_REQUESTS.value)

    def request_with_retry(self) -> Optional[Response]:
        response = self.make_request()
        return self.retry(response)
