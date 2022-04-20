#!/bin/bash


for i in {1..9}
do
./ask ../data/set4/a$i.txt 1 > log/log$i.txt;
done