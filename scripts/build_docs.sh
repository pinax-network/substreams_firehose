#!/usr/bin/env bash

source .venv/bin/activate

pdoc substreams_firehose -o docs/ -d google -t docs/ \
	--logo https://raw.githubusercontent.com/pinax-network/substreams_firehose/main/docs/logo.png \
	--logo-link https://github.com/pinax-network/substreams_firehose/ \
	--footer-text "$(printf "%s (v%s) made with ♡ by %s for Pinax" $(hatch project metadata | jq -r .name,.version,.authors[0].name))"