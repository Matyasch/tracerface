#!/usr/bin/env bash
set -e


ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIRTUALENV_DIR="$ROOT_DIR/bin-python"

function usage() {
    echo "usage: $0 [-h --help] [-d --debug] [-l --routes-logging]"
    echo
    echo
    echo "This script is a wrapper around main.py and its dependecnies"
    echo
    echo "Run this script if you want to start the application in a"
    echo "virtual environment with all the required python package"
    echo "dependencies preinstalled."
    echo
    echo "NOTE: Running this script for the first time may take a"
    echo "considerable amount of time. If you have the needed python"
    echo "packages installed already, feel free to run main.py directly"
    echo
    echo
    echo "valid options:"
    echo "      -h, --help              Show this message"
    echo "      -d, --debug             Start server in debug mode"
    echo "      -l, --routes-logging    Show routes access logging in the console"

}


start_command="python3 $ROOT_DIR/main.py"

args=$(getopt -l help,debug,routes-logging -o hdl -- "$@")
eval set -- "$args"
while [ $# -ge 1 ];
do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--debug)
            start_command+=" --debug"
            shift
            ;;
        -l|--routes-logging)
            start_command+=" --routes-logging"
            shift
            ;;
    esac
    shift
done

python3 -m venv "$VIRTUALENV_DIR"
source "$ROOT_DIR/bin-python/bin/activate"
pip3 --disable-pip-version-check install --no-cache-dir --requirement requirements.txt > bin-python/pip-install.log

$start_command
