#!/bin/sh
set -e
cd "$(dirname "$0")"
export PATH="$PATH:$HOME/.local/bin"
INSTALLED="installed.conf"
if [ ! -e "$INSTALLED" ]; then
	pip3 install --user pipenv
	pipenv install --three --venv
fi
touch "$INSTALLED"
export PYTHONPATH=$PYTHONPATH:$(pwd)
pipenv shell
