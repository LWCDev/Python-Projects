#!/bin/bash
# Basic while loop
#read pause
export PYTHONPATH="/c/Users/lewis.welshclark/PycharmProjects/Projects"
while :
do
	echo "Sleeping for 30 seconds - Press [CTRL+C] to stop.."
	python Lewis_dnb_pagination.py
	sleep 30
done