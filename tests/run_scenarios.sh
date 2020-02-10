#!/bin/bash -xeu

tmpfile=$(mktemp)

cleanup() {
    rm ${tmpfile}
}

trap cleanup EXIT

for scenario in scenarios/*; do
    diff.py ${scenario}/{old,new} > ${tmpfile}
    diff ${scenario}/import/diff.txt ${tmpfile}
done

