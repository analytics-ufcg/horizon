#!/bin/bash

while true
do

for i in {1..8}
do
yes > /dev/null &

sleep $[ ( $RANDOM % 10 )  + 1 ]m
done

killall yes

sleep $[ ( $RANDOM % 10 )  + 1 ]m

done
