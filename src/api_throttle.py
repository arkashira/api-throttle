import time
from dataclasses import dataclass
from threading import Lock
from functools import wraps

@dataclass
class TokenBucket:
    capacity: int
    rate: int
    current_amount: int = 0
    last_update: float = 0

    def get_token(self):
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        self.current_amount = min(self.capacity, self.current_amount + elapsed * self.rate)
        if self.current_amount < 1:
            return False
        self.current_amount -= 1
        return True

    def wait_for_token(self):
        while not self.get_token():
            time.sleep(0.1)

class Throttle:
    def __init__(self, concurrency_limit, rate):
        self.concurrency_limit = concurrency_limit
        self.rate = rate
        self.token_bucket = TokenBucket(concurrency_limit, rate)
        self.lock = Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                self.token_bucket.wait_for_token()
            return func(*args, **kwargs)
        return wrapper

    def get_metrics(self):
        return {
            'concurrency_limit': self.concurrency_limit,
            'current_usage': self.token_bucket.capacity - self.token_bucket.current_amount,
            'rate': self.rate
        }
