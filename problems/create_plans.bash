#!/bin/bash

# arguments expected:
# - path from pwd to the domain and problem files
# - name of the domain file

path=$(pwd)/$1
domain=$path/$2

# Makes a result directory if it doesn't exist
mkdir -p $path/results;
# Loops through problem file in directory and solves using optic-cplex
for FILE in $(ls $path/instances/);
do  
    echo "Solving Problem ${FILE}";
    timeout 600 optic-cplex $domain ${path}/instances/${FILE} > ${path}/results/$1_${FILE%.*}_plan.pddl;
done