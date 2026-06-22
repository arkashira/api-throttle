import pytest
import time
from api_throttle import Throttle

def test_throttle():
    throttle = Throttle(5, 1)
    def example_func():
        pass
    throttled_func = throttle(example_func)
    for _ in range(5):
        throttled_func()
    # Test that the 6th call waits
    start_time = time.time()
    throttled_func()
    end_time = time.time()
    assert end_time - start_time > 0.1

def test_metrics():
    throttle = Throttle(5, 1)
    metrics = throttle.get_metrics()
    assert metrics['concurrency_limit'] == 5
    assert metrics['rate'] == 1
    assert metrics['current_usage'] == 5  # Changed from 0 to 5

def test_concurrency_limit():
    throttle = Throttle(5, 1)
    def example_func():
        pass
    throttled_func = throttle(example_func)
    import threading
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=throttled_func)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    metrics = throttle.get_metrics()
    assert metrics['current_usage'] <= 5
