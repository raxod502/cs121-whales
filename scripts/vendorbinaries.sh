#!/bin/sh

CDPATH=

cd -- "$(dirname -- "$0")"
cd ..

while read url; do
    if [ -n "$url" ]; then
        curl -L "$url" | tar -xz
    fi
done < .vendor_urls
