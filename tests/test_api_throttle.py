import pytest
from api_throttle import ApiThrottle, Response, StatusCode

def test_exponential_backoff():
    throttle = ApiThrottle()
    throttle.backoff_interval = 1
    throttle.exponential_backoff()
    assert throttle.backoff_interval == 2

def test_exponential_backoff_with_jitter():
    throttle = ApiThrottle()
    throttle.backoff_interval = 1
    original_backoff_interval = throttle.backoff_interval
    throttle.exponential_backoff()
    assert throttle.backoff_interval > original_backoff_interval

def test_retry():
    throttle = ApiThrottle()
    response = Response(StatusCode.TOO_MANY_REQUESTS.value)
    new_response = throttle.retry(response)
    assert new_response.status_code == StatusCode.TOO_MANY_REQUESTS.value

def test_retry_max_retries():
    throttle = ApiThrottle(max_retries=1)
    response = Response(StatusCode.TOO_MANY_REQUESTS.value)
    new_response = throttle.retry(response)
    assert new_response.status_code == StatusCode.TOO_MANY_REQUESTS.value
    new_response = throttle.retry(response)
    assert new_response is None

def test_request_with_retry():
    throttle = ApiThrottle()
    response = throttle.request_with_retry()
    assert response.status_code == StatusCode.TOO_MANY_REQUESTS.value

def test_request_with_retry_success():
    class MockApiThrottle(ApiThrottle):
        def make_request(self):
            return Response(StatusCode.SUCCESS.value)

    throttle = MockApiThrottle()
    response = throttle.request_with_retry()
    assert response.status_code == StatusCode.SUCCESS.value
