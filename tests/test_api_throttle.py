from datetime import datetime, timedelta
from api_throttle import Throttle

def test_throttle_acquire_release():
    throttle = Throttle(limit=5, window=timedelta(seconds=1))
    for _ in range(5):
        assert throttle.acquire()
    assert not throttle.acquire()
    throttle.release()
    assert throttle.acquire()

def test_throttle_window():
    throttle = Throttle(limit=5, window=timedelta(seconds=1))
    for _ in range(5):
        throttle.acquire()
    throttle.calls[0] = datetime.now() - timedelta(seconds=2)
    assert throttle.acquire()
