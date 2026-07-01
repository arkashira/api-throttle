<h3 align="center">🛠️ api-throttle</h3>

<div align="center">
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Build Status](https://img.shields.io/badge/Build-passing-green.svg)](https://github.com/axentx/api-throttle)
  [![Stars](https://img.shields.io/github/stars/axentx/api-throttle?style=social)](https://github.com/axentx/api-throttle)
</div>

---

# 🚀 api-throttle
**Power Python developers with intelligent API rate limiting and handling.** A lightweight Python library that provides exponential backoff with jitter for retrying HTTP 429 (Too Many Requests) responses.

## Why api-throttle?
- **Reliable**: Implements proven exponential backoff algorithm to handle rate limiting gracefully
- **Efficient**: Adds random jitter to prevent thundering herd problems when multiple clients retry simultaneously
- **Smart**: Automatically respects Retry-After headers from API responses for optimal retry timing
- **Simple**: Clean, intuitive API that wraps around your existing HTTP calls with minimal code changes
- **Tested**: Comprehensive test suite ensures reliability across different rate limiting scenarios
- **Lightweight**: Minimal dependencies and optimized for performance in production environments
- **Flexible**: Configurable parameters to match different API rate limiting policies

## Feature Overview
| Feature | Description |
|---------|-------------|
| Exponential Backoff | Automatically increases wait time between retries to avoid overwhelming APIs |
| Random Jitter | Adds randomness to retry timing to prevent synchronized retry attempts |
| Retry-After Support | Parses and respects Retry-After headers from API responses |
| Customizable Retries | Configurable maximum retry attempts and base wait time |
| Decorator Interface | Simple decorator to wrap existing API functions with rate limiting |
| Context Manager | Alternative usage pattern with context manager for fine-grained control |
| Logging Support | Built-in logging for monitoring retry attempts and rate limiting events |

## Tech Stack
- Python 3.8+
- Poetry for dependency management
- pytest for testing

## Project Structure
```
api-throttle/
├── business/          # Business logic and requirements
├── docs/             # Documentation files
├── src/              # Source code
└── tests/            # Test suite
```

## Getting Started
Install the library using Poetry:

```bash
poetry add api-throttle
```

Basic usage example:

```python
from api_throttle import throttle_api_call

@throttle_api_call(max_retries=3)
def make_api_call(url):
    # Your API call logic here
    response = requests.get(url)
    return response.json()
```

Run tests:

```bash
po