set -e

# BCC package needs to be available as it can not be installed with pip
[ -f "/usr/lib/python3/dist-packages/bcc/__init__.py" ] && {
    export PYTHONPATH="$PYTHONPATH:/usr/lib/python3/dist-packages"
} || {
    echo "Please install the python3-bcc package"
    exit 1
}
