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
    if [[ ! -e ${scenario}/import/documents.txt ]]; then
        continue
    fi
    if [[ -e ${scenario}/import/diff_rc ]]; then
        diff_rc=$(cat ${scenario}/import/diff_rc)
    else
        diff_rc=0
    fi
    assertRC ${diff_rc} diff.py ${scenario}/{old,new} > ${tmpfile}
    diff ${scenario}/import/diff.txt ${tmpfile}
done

