#!/bin/sh
set -eu

python seed.py
exec python start.py
