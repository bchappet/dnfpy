#!/bin/bash

EXEC="python"
modules="core model"

for module in $modules
do
        echo "Test "$module
        $EXEC ./test_dnfpy/$module/test_suite.py
done



