#!/usr/bin/env bash

cd $(readlink -f "$(dirname "$0")/..")
python setup.py sdist upload -r nexus

