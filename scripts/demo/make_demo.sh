#!/usr/bin/env bash

if command -v gum >/dev/null 2>&1 ; then
	echo "$(gum --version)"
else
	echo "gum not found : please see https://github.com/charmbracelet/gum#installation"
	exit
fi

DEMO_FOLDER="scripts/demo"

gum format '**[*] Choose a `.tape` file to render :**'
TAPE_FILE=$(gum file "${DEMO_FOLDER}" --file)

if [ "${TAPE_FILE}" ]; then
	if vhs validate "${TAPE_FILE}" >/dev/null 2>&1; then
		FILENAME=$(basename "${TAPE_FILE}" .tape)
		gum spin --spinner meter --title="$(gum format '*Running the tape...*')" -- vhs "${TAPE_FILE}"
		gum spin --spinner meter --title="$(gum format '*Adding background logo...*')" --show-output -- \
			ffmpeg -y -i $DEMO_FOLDER/$FILENAME.mp4 -i $DEMO_FOLDER/logo.svg \
			-filter_complex "[1]format=rgba,colorchannelmixer=aa=0.1[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p" \
			-c:a copy $DEMO_FOLDER/$FILENAME_demo.mp4
		gum spin --spinner meter --title="$(gum format '*Cleaning up...*')" -- rm $DEMO_FOLDER/$FILENAME.mp4
		gum format "**[+] Done !**"
	else
		gum format "**[ERROR] Invalid file chosen**"
		exit
	fi
else
	gum format '**[!] No `.tape` file selected, aborting...**'
fi