#!/usr/bin/env bash

./convert_epub_to_mobi.py
source ./env
./send_to_kindle.py
