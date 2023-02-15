#!/usr/bin/env bash

DEMO_FOLDER="scripts/demo"

vhs < $DEMO_FOLDER/scripted_demo.tape
ffmpeg -y -i $DEMO_FOLDER/demo.mp4 -i $DEMO_FOLDER/logo.svg -filter_complex "[1]format=rgba,colorchannelmixer=aa=0.1[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p" -c:a copy $DEMO_FOLDER/substreams_firehose_eth_config_demo.mp4
rm $DEMO_FOLDER/demo.mp4
rm -rf jsonl/
rm substreams_firehose/config/firehose/eth.hjson