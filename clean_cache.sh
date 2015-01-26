#!/bin/bash

folder=.wikipedia_cache
n=`ls -1 $folder/* | wc -l | cut -d' ' -f1`
echo $n files cached removed
rm -rf $folder
