#!/bin/bash

TEST_FOLDER="tests"

passed=0

for t in $TEST_FOLDER/*;
do
    python3.8 FRISCGenerator.py < $t/Test.in > /tmp/Test.out
    diff -s $t/Test.out /tmp/Test.out

    if [[ $(diff -s $t/Test.out /tmp/Test.out ) == *"identical"* ]];
    then
        passed=$(($passed + 1))
    fi
done

total=$(find $TEST_FOLDER/* -type d | wc -l)
echo -e "\nPassed: $passed \nTotal : $total"

