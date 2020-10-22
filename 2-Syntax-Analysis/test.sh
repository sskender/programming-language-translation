#!/bin/bash

TEST_FOLDER="tests"

for t in $TEST_FOLDER/*;
do
    python3.8 SintaksniAnalizator.py < $t/test.in > /tmp/test.out
    diff -s $t/test.out /tmp/test.out
done
