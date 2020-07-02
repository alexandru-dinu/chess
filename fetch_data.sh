#!/bin/bash

LIST="https://database.lichess.org/standard/list.txt"

mkdir data

if [ ! -f list.txt ]; then
    wget -q $LIST
else
    wget -q $LIST -O list.txt.tmp
    diff list.txt list.txt.tmp &> /dev/null

    if [ $? -ne 0 ]; then
        echo 'Updated list.'
    else
        echo 'List is up-to-date.'
    fi

    mv list.txt.tmp list.txt
fi


N=75
aria2c -s 16 -x 16 $(sed "${N}q;d" list.txt) -d data/
