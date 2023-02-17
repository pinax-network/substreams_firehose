Output scripts/demo/set_api_keys.mp4

Set FontFamily "Space Mono"
Set Theme {
	"name":"Pinax",
	"background":"#000000",
	"foreground":"#ffffff",
	"black":"#000000",
	"blue":"#6923ea",
	"green":"#6923ea",
	"yellow":"#ef758c",
	"brightYellow":"#8fffe9"
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
Type "python -m substreams_firehose.config"
Sleep 1.5s
Enter

# === Open menu and enter stub config editing ===
Sleep 2.5s
Ctrl+X
Sleep 1.5s
Enter
Sleep 1.5s
Down
Sleep 500ms
Enter

# === Edit `Pinax` authentication provider ===
Sleep 1.5s
Down
Sleep 500ms
Enter
Sleep 1s
Enter

# === Editing API key field ===
Sleep 1.5s
Down
Sleep 500ms
Enter
Sleep 250ms
Backspace@100ms 10
Backspace@50ms 20
Type 'dummy'
Sleep 1s
Tab@250ms 2
Enter

# === Exiting authentication provider editing ===
Sleep 1s
Down@250ms 3
Sleep 150ms
Enter

# === Validating changes ===
Sleep 1s
Down@250ms 4
Sleep 150ms
Enter
Sleep 6s
Tab
Sleep 250ms
Right
Sleep 250ms
Enter

# === Confirm main configuration overwrite ===
Sleep 1.5s
Tab
Sleep 250ms
Right
Sleep 250ms
Enter
Sleep 1s
Tab
Sleep 250ms
Enter

Sleep 3s