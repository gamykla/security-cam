#!/bin/bash
set -ex

if [ "$1" = 'camserver.sh' ]; then
    camserver.sh
fi

exec "$@"

