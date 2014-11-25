#!/bin/bash

#clean *.pyc and *~

find . -name "*.pyc" -type f -delete
find . -name "*~" -type f -delete
