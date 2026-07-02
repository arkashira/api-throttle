<h3 align="center">🛠️ api-throttle</h3>
<div align="center">
  <a href="https://github.com/axentx/api-throttle/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"/></a>
  <a href="https://github.com/axentx/api-throttle"><img src="https://img.shields.io/github/languages/top/axentx/api-throttle?color=blue" alt="Language"/></a>
  <a href="https://github.com/axentx/api-throttle/actions/workflows/test.yml"><img src="https://github.com/axentx/api-throttle/actions/workflows/test.yml/badge.svg" alt="Build"/></a>
  <a href="https://github.com/axentx/api-throttle/stargazers"><img src="https://img.shields.io/github/stars/axentx/api-throttle?style=social" alt="Stars"/></a>
</div>

---

# 🚀 api-throttle

**Empower Python developers with intelligent rate-limiting for external API integrations.**

## Why api-throttle?

- **Smart Retries**: Implements exponential backoff with jitter to prevent thundering herd issues.
- **Retry-After Support**: Respects the `Retry-After` header from HTTP 429 responses for smarter retry timing.
- **Lightweight & Simple**: Minimal overhead with clean, reusable utility functions for wrapping API calls.
- **Sandbox Tested**: Real-world tested in simulated environments to ensure reliability.
- **Developer-Focused**: Built for Python developers integrating with third-party APIs that enforce rate limits.
- **Production Ready**: Designed for use in production systems where robustness matters.
- **Well Documented**: Clear documentation and examples included for easy adoption.

## Feature Overview

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Exponential Backoff      | Gradually increases delay between retries to reduce load on APIs.          |
| Jitter Addition          | Randomizes delays to avoid synchronized retry storms.                      |
| Retry-After Header       | Uses server-provided retry timing when available.                          |
| Easy Integration         | Simple decorator and function wrappers for API call decoration.            |
| Test Coverage            | Full test suite using pytest ensures stability and correctness.            |

## Tech Stack

- **Python**: Core implementation language.
- **Poetry**: Dependency management and packaging.
- **pytest**: Testing framework for unit and integration tests.

## Project Structure

```
api-throttle/
├── business/           # Business logic or domain-specific code (if any)
├── docs/               # Documentation files
├── src/                # Source code root
│   └── api_throttle/   # Main module
├── tests/              # Unit and integration tests
├── pyproject.toml      # Project configuration and dependencies
└── README.md           # This file
```

## Getting Started

Install the package using Poetry:

```bash
poetry install
```

Run the tests:

```bash
poetry run pytest tests/
```

Use in your Python project:

```python
from api_throttle import with_retry

@with_retry(max_retries=5, base_delay=1)
def fetch_data(url):
    response = requests.get(url)
    return response.json()
```

## Deploy

This project is a Python library intended for installation via Poetry or pip. No deployment steps required beyond publishing to PyPI or installing locally.

To publish to PyPI:

```bash
poetry build
poetry publish
```

## Status

📦 Early-stage development.  
Latest commit: `810edaf` — *readme-keeper: generate proper project README*

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.