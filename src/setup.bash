#!/bin/bash

shopt -s expand_aliases
unzip="unzip files.zip"
eval $unzip
path=$(eval "pwd")
str="alias AIDE=\x22cd $path/ && python3 -m UI.py\x22"
ali=$(echo -e $str)
HOME=$(eval "cd")
echo $ali>> $HOME/.profile.d/interactive/pre
