#!/usr/bin/env bash

echo "running unit tests"
python3 -m pytest tests/unit/

if [ "$EUID" -ne 0 ]; then
    echo "Run with sudo for integration tests too"
else
    echo "preparing integration test resources"
    gcc -ggdb3 -O0 -fno-omit-frame-pointer \
        -o tests/integration/resources/test_application \
        tests/integration/resources/test_application.c

    echo "running integration tests"
    python3 -m pytest tests/integration/

    echo "tearing down integration test resources"
    rm tests/integration/resources/test_application
fi
