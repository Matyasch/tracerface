#!/usr/bin/env bash
set -e


ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIRTUALENV_DIR="$ROOT_DIR/bin-python"

function usage() {
    echo "usage: $0 [-h --help] [-d --debug] [-l --routes-logging]"
    echo
    echo "This script is a wrapper around main.py and its dependecnies"
    echo
    echo "valid options:"
    echo "      -h, --help              Show this message"
    echo "      -d, --debug             Start server in debug mode"
    echo "      -l, --routes-logging    Show routes access logging in the console"

}

start_command="python3 $ROOT_DIR/main.py"

args=$(getopt -l help,debug,routes-loggin -o hdl -- "$@")
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

source "$ROOT_DIR/bcc-env.inc.sh"

python3 -m virtualenv "$VIRTUALENV_DIR"
source "$ROOT_DIR/bin-python/bin/activate"
pip3 --disable-pip-version-check install --no-cache-dir --requirement requirements.txt > "$VIRTUALENV_DIR/pip-install.log"

$start_command
