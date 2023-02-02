#!/usr/bin/env bash

sort_jsonl_output(){
	jq -s -c 'sort_by(.number)[]' $1 > jsonl/sorted.jsonl
	mv jsonl/sorted.jsonl $1
}

# Generic function to run Pyfirehose
run_test(){
	python -m pyfirehose $1 $2 \
	--grpc-entry $3 \
	--stub scripts/benchmarking/test_configs/$4.hjson \
	--out-file jsonl/$4.jsonl \
	--quiet \
	"${@:5}"
	# --log logs/$4.log \
	# --overwrite-log \

	# sort_jsonl_output jsonl/$4.jsonl
}
export -f run_test

# ========================================
# === Large block range test functions ===
# ========================================

run_large_dfuse(){
	run_test $START $END antelope_firehose_v1 dfuse
}
export -f run_large_dfuse

run_large_firehose(){
	run_test $START $END antelope_firehose_v2 firehose
}
export -f run_large_firehose

run_large_substream(){
	run_test $START $END antelope_firehose_v2 substream -p default_substream_processor
}
export -f run_large_substream

# ========================================
# === Burst block range test functions ===
# ========================================

run_burst_dfuse(){
	for s in $(seq $START $NUM_BLOCKS $END); do
		run_test $s $(($s + $NUM_BLOCKS)) antelope_firehose_v1 dfuse
	done
}
export -f run_burst_dfuse

run_burst_firehose(){
	for s in $(seq $START $NUM_BLOCKS $END); do
		run_test $s $(($s + $NUM_BLOCKS)) antelope_firehose_v2 firehose
	done
}
export -f run_burst_firehose

run_burst_substream(){
	for s in $(seq $START $NUM_BLOCKS $END); do
		run_test $s $(($s + $NUM_BLOCKS)) antelope_firehose_v2 substream -p default_substream_processor
	done
}
export -f run_burst_substream

# ================================================
# === Random block range access test functions ===
# ================================================

run_random_access_dfuse(){
	for i in $(seq 1 $ITERATIONS); do
		RANDOM_START=`shuf -i $START-$END -n 1`
		run_test $RANDOM_START $(($RANDOM_START + $NUM_BLOCKS)) antelope_firehose_v1 dfuse
	done
}
export -f run_random_access_dfuse

run_random_access_firehose(){
	for i in $(seq 1 $ITERATIONS); do
		RANDOM_START=`shuf -i $START-$END -n 1`
		run_test $RANDOM_START $(($RANDOM_START + $NUM_BLOCKS)) antelope_firehose_v2 firehose
	done
}
export -f run_random_access_firehose

run_random_access_substream(){
	for i in $(seq 1 $ITERATIONS); do
		RANDOM_START=`shuf -i $START-$END -n 1`
		run_test $RANDOM_START $(($RANDOM_START + $NUM_BLOCKS)) antelope_firehose_v2 substream -p default_substream_processor
	done
}
export -f run_random_access_substream

# ============================
# === Test suite functions ===
# ============================

run_large_test(){
	START=222000000
	NUM_BLOCKS=2500
	END=$(($START + $NUM_BLOCKS))
	echo "Running large range block test from #$START to #$END ($NUM_BLOCKS blocks) on Antelope chain..."

	export START
	export END

	echo "=== DFUSE ==="
	hyperfine --shell=bash run_large_dfuse --runs 2

	echo "=== FIREHOSE ==="
	hyperfine --shell=bash run_large_firehose --runs 2

	echo "=== SUBSTREAMS ==="
	hyperfine --shell=bash run_large_substream --runs 2
}

run_burst_test(){
	START=230000000
	NUM_BLOCKS=25
	ITERATIONS=100
	END=$(($START + $NUM_BLOCKS*$ITERATIONS))
	echo "Running burst range block test from #$START to #$END ($NUM_BLOCKS blocks for $ITERATIONS iterations) on Antelope chain..."

	export START
	export NUM_BLOCKS
	export END

	echo "=== DFUSE ==="
	hyperfine --shell=bash run_burst_dfuse --runs 2

	echo "=== FIREHOSE ==="
	hyperfine --shell=bash run_burst_firehose --runs 2

	echo "=== SUBSTREAMS ==="
	hyperfine --shell=bash run_burst_substream --runs 2
}

run_random_access_test(){
	START=240000000
	NUM_BLOCKS=100
	ITERATIONS=25
	END=250000000
	echo "Running random access block range test between #$START and #$END ($NUM_BLOCKS blocks chosen randomly for $ITERATIONS iterations) on Antelope chain..."

	export START
	export NUM_BLOCKS
	export ITERATIONS
	export END

	echo "=== DFUSE ==="
	hyperfine --shell=bash run_random_access_dfuse --runs 2

	echo "=== FIREHOSE ==="
	hyperfine --shell=bash run_random_access_firehose --runs 2

	echo "=== SUBSTREAMS ==="
	hyperfine --shell=bash run_random_access_substream --runs 2
}

# =========================
# === Dependency checks ===
# =========================

echo 'Checking dependencies...'
if command -v hyperfine >/dev/null 2>&1 ; then
	echo "$(hyperfine --version)"
else
	echo "hyperfine not found : please see https://github.com/sharkdp/hyperfine#installation"
	exit
fi

if command -v gum >/dev/null 2>&1 ; then
	echo "$(gum --version)"
else
	echo "gum not found : please see https://github.com/charmbracelet/gum#installation"
	exit
fi

# ============
# === Main ===
# ============

# Activate python environnement
source .venv/bin/activate

# From https://stackoverflow.com/a/3403786
# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee -i scripts/benchmarking/results/tmp)
exec 2>&1

echo -e "\nChoose a test suite to run :"
TEST_MODE=$(gum choose "Large" "Burst" "Random access" "All")

case $TEST_MODE in
	Large)
		run_large_test
		;;

	Burst)
		run_burst_test
		;;

	"Random access")
		run_random_access_test
		;;

	All)
		run_large_test
		run_burst_test
		run_random_access_test
		;;

	*)
		echo "No test suite selected, exiting..."
		exit
esac

# Move temporary output to named file in `results/` folder
mv scripts/benchmarking/results/tmp scripts/benchmarking/results/$(date +"%d-%m-%Y")_$(echo -e "${TEST_MODE}" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]').txt

# Cleanup Pyfirehose output files
rm -rf jsonl/