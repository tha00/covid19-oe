#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

PACKAGE_DIR=../build/tmp/
mkdir -p "$PACKAGE_DIR"

pip3 install --target="$PACKAGE_DIR" -r ../requirements.txt

cp ../lambda_function.py "$PACKAGE_DIR"/

cd $PACKAGE_DIR || exit
zip -r ../lambda_function.zip .

cd ..
rm -rf tmp
