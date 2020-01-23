#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# For macOS, so that I can call ebook-converter

PATH="$PATH:/Applications/calibre.app/Contents/MacOS/"

EPUBS="$(pwd)/Epubs/*.epub"
MOBI="$(pwd)/Mobi/"
for book in ${EPUBS}; do
    title=$(basename "${book}" .epub)
    if [[ ${title} == ".gitkeep" ]]; then
        continue
    fi
    if [ ! -f "${book}" ]; then
        continue
    fi
    echo "Converting ${title}.epub ..."
    ebook-convert ${book} ${MOBI}/${title}.mobi >/dev/null
    rename 's/\(z-lib\.org\)//' "${MOBI}/${title}.mobi" &>/dev/null
done

rm -rf ${EPUBS}
