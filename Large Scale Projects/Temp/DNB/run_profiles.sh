#!/bin/bash
# Basic while loop
#read pause
export PYTHONPATH="/c/Users/lewis.welshclark/PycharmProjects/Projects"
while :
do
	echo "Sleeping for 120 seconds - Press [CTRL+C] to stop.."
	python Lewis_dnb_profiles_mp_v2_functioning.py
	sleep 120
done