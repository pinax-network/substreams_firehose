#!/usr/bin/env bash

source ../../.venv/bin/activate

PROTOFILES=$(find . -iname *.proto)

python -m grpc_tools.protoc -I. --python_out=generated/ --grpc_python_out=generated/ $PROTOFILES