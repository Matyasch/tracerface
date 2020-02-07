#!/usr/bin/env bash
set -e


ENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# BCC package needs to be available as it can not be installed with pip
function check_bcc_available() {
    [ -f "/usr/lib/python3/dist-packages/bcc/__init__.py" ] && {
        export PYTHONPATH="$PYTHONPATH:/usr/lib/python3/dist-packages"
    } || {
        echo "Please install the python3-bcc package"
        exit 1
    }
}

# Download trace.py from BCC repo because that is the only script we need
function download_trace_script() {
    wget -q "https://raw.githubusercontent.com/iovisor/bcc/master/tools/trace.py" -O "$ENV_DIR/bcc_trace.py"
    chmod +x "$ENV_DIR/bcc_trace.py"
}

check_bcc_available
download_trace_script
