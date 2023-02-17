#!/usr/bin/env bash

if command -v gum >/dev/null 2>&1 ; then
	echo "$(gum --version)"
else
	echo "gum not found : please see https://github.com/charmbracelet/gum#installation"
	exit
fi

# Activate python environnement
source .venv/bin/activate

PACKAGE_VERSION=$(gum input --header="$(gum format "**[*] Set the package version :**")" --value="$(hatch version)")

if [ "${PACKAGE_VERSION}" ]; then
	hatch version "${PACKAGE_VERSION}"
else
	gum format "**[ERROR] No package version set, aborting...**"
	exit
fi

gum format "**[*] Choose a publishing repo :**"
PUBLISH_TARGET=$(gum choose "test" "main")

if [ "${PUBLISH_TARGET}" ]; then
	gum spin --spinner meter --title="$(gum format '*Cleaning `dist/` artifacts...*')" -- rm -rf dist/
	gum spin --spinner meter --title="$(gum format '*Building artifacts...*')" --show-output -- hatch build
	gum spin --spinner meter --title="$(gum format "*Publishing to '${PUBLISH_TARGET}' repo...*")" --show-output -- hatch publish -r $PUBLISH_TARGET
	gum format "**[+] Done !**"
else
	gum format "**[ERROR] No publishing repo selected, aborting...**"
fi