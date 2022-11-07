#!/usr/bin/env bash

# Extracts daily transactions emitted from EOSNation block producer's addresses
ACCOUNTS=("eosio.bpay" "eosio.vpay")
YESTERDAY=$(date +"%Y-%m-%dT%H:%M:%S%:z" -d "yesterday 0")
TODAY=$(date +"%Y-%m-%dT%H:%M:%S%:z" -d "today 0")

FILENAME=$(date +"%Y-%m-%d" -d "yesterday 0")
OUTFILE="jsonl/producerpay/$FILENAME.jsonl"

if [ ! -f "$OUTFILE" ]
then
	echo "bash -- Extracting data for '${ACCOUNTS[@]}' between ${YESTERDAY} and ${TODAY}"

	# Activate python environnement
	source .venv/bin/activate

	# Uses Bash expansion to add the list of accounts as a JSON-like array to the filter, excluding those accounts from transactions destination.
	time python3 main.py $YESTERDAY $TODAY \
		-i "receiver in [$( printf "'%s'," "${ACCOUNTS[@]}" )] && action == 'transfer'" \
		-x "data['to'] in [$( printf "'%s'," "${ACCOUNTS[@]}" )]" \
		-o "$OUTFILE"\
		"$@"
else
	echo "Data already extracted for $FILENAME (see $OUTFILE)"
fi