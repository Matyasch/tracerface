#!/usr/bin/env bash
set -e


ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIRTUALENV_DIR="$ROOT_DIR/.venv"

if ! [ -f "/usr/share/bcc/tools/trace" ]; then
    echo "Please install the bcc-tools package"
    exit 1
fi

if ! [ -f "/usr/lib/python3/dist-packages/bcc/__init__.py" ]; then
    echo "Please install the python3-bcc package"
    exit 1
fi

python3 -m venv "$VIRTUALENV_DIR"
source "$VIRTUALENV_DIR/bin/activate"
pip install -r requirements.txt > "$VIRTUALENV_DIR/pip-install.log"

$ROOT_DIR/main.py $@
