#!/usr/bin/env bash

# Activate python environnement
source .venv/bin/activate

rm -rf dist/
hatch build
hatch publish -r test