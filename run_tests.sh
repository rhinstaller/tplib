#!/bin/bash -xeu

export PYTHON_PATH=`pwd`
export PATH=$PATH:`pwd`
pushd tests

./run_scenarios.sh

popd
