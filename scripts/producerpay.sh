#!/usr/bin/env bash

# Extracts daily transactions emitted from EOSNation block producer's addresses
ACCOUNTS=("eosio.bpay" "eosio.vpay")
YESTERDAY=`date +"%Y-%m-%dT%H:%M:%S%:z" -d "yesterday 0"`
TODAY=`date +"%Y-%m-%dT%H:%M:%S%:z" -d "today 0"`

echo "bash -- Extracting data for '${ACCOUNTS[@]}' between ${YESTERDAY} and ${TODAY}"

# Activate python environnement
source .venv/bin/activate

# Uses Bash expansion to add the list of account as a JSON-like array to the filter.
time python3 main.py "${ACCOUNTS[@]}" $YESTERDAY $TODAY \
	-x "data['to'] in [$( printf "'%s'," "${ACCOUNTS[@]}" )]" \
	-o "jsonl/producerpay/$(date +"%Y-%m-%d" -d "yesterday 0").jsonl"\
	"$@"