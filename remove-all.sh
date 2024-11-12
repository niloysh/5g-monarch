#!/bin/bash
WORKING_DIR="$(pwd)"
./remove-monarch-nss.sh
./remove-monarch-core.sh
./remove-external.sh

