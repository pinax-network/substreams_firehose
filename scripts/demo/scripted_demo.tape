Output scripts/demo/demo.mp4

Set FontFamily "Space Mono"
Set Theme {
	"name":"Pinax",
	"background":"#000000",
	"foreground":"#ffffff",
	"black":"#000000",
	"blue":"#ef758c",
	"brightBlue":"#6923ea",
	"green":"#8fffe9",
	"yellow":"#8fffe9"
}
Set FontSize 24
Set Width 2400
Set Height 1200
Set Framerate 60
Set PlaybackSpeed 0.35

# === Setup ===
Hide
Type "source .venv/bin/activate"
Enter
Show

# === Entering config UI ===
Type "python -m pyfirehose.config"
Sleep 1.5s
Enter

# === Showcase main config ===
Sleep 2s
Down@100ms 20
Sleep 1s
Down@75ms 30

# === Open menu and enter stub config editing ===
Sleep 1s
Ctrl+X
Sleep 1s
Down
Sleep 1s
Enter

# === Endpoint selection ===
Sleep 2s
Down@250ms 5
Sleep 500ms
Space
Sleep 500ms
Down@125ms 11
Sleep 1s
Enter

# === Save file ===
Sleep 1s
Enter
# --- 'Pyfirehose' folder ---
Sleep 1s
Down@150ms 2
Right
Sleep 500ms
Enter
# --- 'config' folder ---
Sleep 500ms
Down
Sleep 500ms
Right
Sleep 500ms
Enter
# --- 'firehose' folder ---
Sleep 500ms
Down
Sleep 500ms
Enter
# --- Filling out filename ---
Sleep 500ms
Tab
Type "/eth.hjson"
Sleep 1s
Enter
# --- Pressing OK ---
Sleep 500ms
Down@150ms 2
Sleep 1s
Enter

# === Service selection ===
Sleep 2s
Down@250ms 4
Sleep 500ms
Space
Sleep 500ms
Down@150ms 2
Sleep 1s
Enter

# === Method selection ===
Sleep 1s
Down@150ms 2
Sleep 1s
Enter

# === Inputs settings ===
Sleep 1s
Down
Sleep 500ms
Enter
# --- Checking 'final_blocks_only' checkbox
Sleep 2s
Space
Sleep 500ms
Down@150ms 2
Sleep 200ms
Enter
# --- Pressing OK ---
Sleep 500ms
Down@150ms 3
Sleep 1s
Enter

# === Outputs settings ===
Sleep 2s
Down@250ms 5
Sleep 500ms
Space
Sleep 500ms
Tab
# --- Checking output fields
# ... 'ver' ...
Sleep 300ms
Down
Space
# ... 'hash' ...
Sleep 300ms
Down
Space
# ... 'number' ...
Sleep 300ms
Down
Space
# ... 'transaction_traces' ...
Sleep 300ms
Down@150ms 4
Space
Sleep 500ms
Type "l"
Sleep 500ms
Down@150ms 6
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down@150ms 2
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down@150ms 3
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down@150ms 2
Space
Sleep 300ms
Down
Space
Sleep 300ms
Down@150ms 4
Sleep 1s
Enter

# === Stub config recap ===
Sleep 2s
Down@100ms 15
Sleep 1s
Tab@150ms 3
Sleep 1s
Enter

# === Savefile info popup ===
Sleep 2s
Tab
Sleep 500ms
Enter

# === Quit ===
Sleep 1s
Tab@150ms 2
Sleep 1s
Enter

# === Show help page ===
Sleep 1s
Type "python -m pyfirehose -h"
Sleep 1.5s
Enter 2

# === Getting ethereum last block ===
Sleep 1s
Type "# Getting latest block number for the Ethereum blockchain"
Sleep 500ms
Enter
Type "LAST_ETH_BLOCK=$(curl -s https://api.blockcypher.com/v1/eth/main | jq .height) && echo $LAST_ETH_BLOCK"
Sleep 1.5s
Enter

# === Starting PyFirehose ===
Sleep 1s
Type "# Starting PyFirehose using the previously created stub configuration file"
Sleep 500ms
Enter
Type "python -m pyfirehose $(($LAST_ETH_BLOCK - 200)) $(($LAST_ETH_BLOCK - 100)) -g eth_mainnet -s pyfirehose/config/firehose/eth.hjson -o jsonl/eth.jsonl"
Sleep 1.5s
Enter

# === Showing the results ===
Sleep 20s
Type "cat jsonl/eth.jsonl | jq --color-output | less --RAW-CONTROL-CHARS"
Sleep 1s
Enter
Sleep 1s
Down@150ms 50
Down@50ms 100
Sleep 2s
Type "q"
Sleep 2s