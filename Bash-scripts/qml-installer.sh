#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "${GREEN}Try to get list of requirements packges..${NC}\n"
var=$(apt list qml-module*)
sleep 1

#IFS=$'\n' y=($var)
IFS=$'\n' read -rd '' -a y <<<"$var"
#printf "${y[1]}\n"

#sorting array
req=()
count=$#
for package in ${y[@]};do 
if [[ $package =~ .*qml.* ]]
then
    #printf "$package\n"
    count+=1
    #req[count]=$package
    req+=("$package")
    printf "${GREEN}$package${NC}\n"
    sleep .1
fi
done

printf "${GREEN}Try to install of requirements packges..${NC}\n"
sleep 2
for package in ${req[@]};do
    eval apt-get install -y $package
done





