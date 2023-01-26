#!/usr/bin/env bash

vhs < scripted_demo.tape
ffmpeg -i demo.mp4 -i logo.svg -filter_complex "[1]format=rgba,colorchannelmixer=aa=0.1[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p" -c:a copy ../pyfirehose_eth_config_demo.mp4
rm demo.mp4
rm -rf jsonl/
rm pyfirehose/config/firehose/eth.hjson