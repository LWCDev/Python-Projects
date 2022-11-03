#!/bin/bash
# Basic while loop
#read pause
export PYTHONPATH="/c/Users/lewis.welshclark/PycharmProjects/Projects"
while :
do
	echo "Sleeping for 240 seconds - Press [CTRL+C] to stop.."
	python lewis_DNB_data_mp_v2_functioning.py
	sleep 240
done