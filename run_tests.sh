#!/bin/bash -xeu

export PYTHONPATH=${PYTHONPATH:-}:`pwd`
export PATH=$PATH:`pwd`
pushd tests

./run_scenarios.sh
./run_unittests.py

popd
