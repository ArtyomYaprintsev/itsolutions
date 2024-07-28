set -xe
isort server --check-only
flake8 server --show-source
pylint server
mypy server
