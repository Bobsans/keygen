#!/usr/bin/env bash

# rm -rf ./dist/

python -m build

rm -rf ./build/
rm -rf ./*.egg-info
