#!/bin/bash -xeu

tmpfile=$(mktemp)
tmpfile2=$(mktemp)
tmpfile3=$(mktemp)

cleanup() {
    rm ${tmpfile}
    rm ${tmpfile2}
    rm ${tmpfile3}
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
    # diff test
    if [[ -e ${scenario}/diff.txt ]]; then
        if [[ -e ${scenario}/diff_rc ]]; then
            diff_rc=$(cat ${scenario}/diff_rc)
        else
            diff_rc=0
        fi
        assertRC ${diff_rc} diff.py ${scenario}/{old,new} > ${tmpfile}
        diff ${scenario}/diff.txt ${tmpfile}
    fi

    # dump test
    if [[ -e ${scenario}/query/diff.txt ]]; then
        if [[ -e ${scenario}/query/query-old_rc ]]; then
            query1_rc=$(cat ${scenario}/query/query-old_rc)
        else
            query1_rc=0
        fi
        if [[ -e ${scenario}/query/query-new_rc ]]; then
            query2_rc=$(cat ${scenario}/query/query-new_rc)
        else
            query2_rc=0
        fi
        if [[ -e ${scenario}/query/diff_rc ]]; then
            diff_rc=$(cat ${scenario}/query/diff_rc)
        else
            diff_rc=0
        fi

        assertRC ${query1_rc} query.py ${scenario}/old > ${tmpfile}
        assertRC ${query2_rc} query.py ${scenario}/new > ${tmpfile2}
        assertRC ${diff_rc} diff ${tmpfile} ${tmpfile2} > ${tmpfile3}
        assertRC 0 diff ${scenario}/query/diff.txt ${tmpfile3}
    fi
done
