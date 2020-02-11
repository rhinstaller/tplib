#!/bin/bash -xeu

tmpfile=$(mktemp)

cleanup() {
    rm ${tmpfile}
}

assertRC() {
    # usage: assertRC RC_CODE [command arg1 arg2 ... argN]
    # exit if RC_CODE doesn't match return code of the command with arguments
    local expected=${1}
    shift
    set +e
    "${@}"
    rc=$?
    set -e
    [[ ${rc} == ${expected} ]]
}

trap cleanup EXIT

for scenario in scenarios/*; do
    diff.py ${scenario}/{old,new} > ${tmpfile}
    diff ${scenario}/import/diff.txt ${tmpfile}
done

