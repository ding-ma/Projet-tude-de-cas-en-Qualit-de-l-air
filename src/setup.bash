#!/bin/bash

xlsxwritter="pip3 install xlsxwriter --user"
echo "installing" $xlsxwritter
eval $xlsxwritter
shopt -s expand_aliases
unzip="unzip files.zip"
eval $unzip
path=$(eval "pwd")
str="alias AIDE=\x22cd $path/ && python3 -m UI.py\x22"
ali=$(echo -e $str)
# If script doesnt work, put the next line in comment as unix system should have $HOME defined.
HOME=$(eval "cd")
echo $ali>> $HOME/.profile.d/interactive/pre
