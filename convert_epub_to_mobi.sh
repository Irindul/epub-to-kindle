#!/usr/bin/env bash

PATH="$PATH:/Applications/calibre.app/Contents/MacOS/"
set -o errexit
set -o pipefail
set -o nounset

EPUBS="$(pwd)/Epubs/*.epub"
MOBI="$(pwd)/Mobi/"
for book in ${EPUBS}; do
    title=$(basename "${book}" .epub)
    if [[ ${title} == ".gitkeep" ]]; then
        continue
    fi
    echo "Converting ${title}.epub ..."
    ebook-convert ${book} ${MOBI}/${title}.mobi >/dev/null
    rename 's/\(z-lib\.org\)//' "${MOBI}/${title}.mobi" &>/dev/null
done

rm -rf ${EPUBS}
