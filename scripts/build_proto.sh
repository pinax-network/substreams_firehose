#!/usr/bin/env bash

# Activate python environnement
source .venv/bin/activate

PROTO_DIR="substreams_firehose/proto"
cd $PROTO_DIR

OUT_DIR="generated"
PROTOFILES=$(find . -iname *.proto)

# Clear generated folder
rm -rf $OUT_DIR/*

# Generate python files from `.proto` definitions
python -m grpc_tools.protoc -I. --python_out=$OUT_DIR --grpc_python_out=$OUT_DIR $PROTOFILES \
							--descriptor_set_out="$OUT_DIR/protos.desc" --include_imports --include_source_info

# Use the [protoletariat](https://github.com/cpcloud/protoletariat) tool to fix relative import issues for generated files.
# See also the [Github issue](https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-977985256) on Google's repo.
protol --in-place --python-out $OUT_DIR raw "$OUT_DIR/protos.desc"