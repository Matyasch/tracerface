#!/usr/bin/env bash
set -e

# Script for running tests properly

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIRTUALENV_DIR="$ROOT_DIR/.venv-test"

if ! [ -f "/usr/lib/python3/dist-packages/bcc/__init__.py" ]; then
    echo "Please install the python3-bcc package"
    exit 1
fi

# Prepare environment
echo "Preparing environment"
python3 -m venv "$VIRTUALENV_DIR"
source "$VIRTUALENV_DIR/bin/activate"
pip install -r requirements-test.txt > "$VIRTUALENV_DIR/pip-install.log"

# Run unit tests
echo "Running unit tests"
python3 -m pytest -vvv -p no:cacheprovider tests/unit/

# Run integration tests
if [ "$EUID" -ne 0 ]; then
    echo "Run with sudo for integration tests too"
else
    echo "Preparing integration test resources"
    gcc -ggdb3 -O0 -fno-omit-frame-pointer \
        -o tests/integration/resources/test_application \
        tests/integration/resources/test_application.c

    echo "Running integration tests"
    python3 -m pytest -vv -p no:cacheprovider tests/integration/

    echo "Tearing down integration test resources"
    rm tests/integration/resources/test_application
fi
