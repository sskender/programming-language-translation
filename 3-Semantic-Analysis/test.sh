#!/bin/bash

TEST_FOLDER="tests"

for t in $TEST_FOLDER/*;
do
    python3.8 SemantickiAnalizator.py < $t/Test.in > /tmp/Test.out
    diff -s $t/Test.out /tmp/Test.out
done
