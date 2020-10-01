#!/bin/bash - 
#===============================================================================
#
#          FILE: extract-test-outputs.sh
# 
#         USAGE: ./extract-test-outputs.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 01/10/20 14:48
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

if [ $# -ne 2 ]; then
    echo "specify in-directory out-directory"
    exit 1
fi

in_dir=$1  # output-simulator-test/*
out_dir=$2


for test_sce_dir in `ls -d $in_dir`; do
    for sim in `ls $test_sce_dir | grep -oe "_[0-9]\+.csv" | grep -oe "[0-9]\+" | sort -nu`; do
        # Create the JSON file name where output is gathered
        test_id=`echo $test_sce_dir | cut -d"/" -f2 | grep -oe "[0-9]\+"`
        # expand sim 02 -> 002
        exp_sim=$(( sim - 1 ))
        while [[ ${#exp_sim} -lt 3 ]]; do exp_sim=0$exp_sim; done
        #out_file=$out_dir"/"$test_id"_"$sim".json"
        out_file=$out_dir"/sim_output_nodes_test_sce"$test_id"_deployment_"$exp_sim".json"


        echo "creating $out_file"


        # Fill the JSON
        cat "$test_sce_dir/rssi_$sim.csv" | sed 's/^/\{"rssi"\: \[/g' | sed 's/$/\]/g' | sed 's/Inf/0/g' >> $out_file
        cat "$test_sce_dir/interference_$sim.csv" | sed 's/^/\[/g' | sed 's/;/],/g' | sed 's/\[Inf/, "interference"\: \[\[Inf/g' | sed 's/Inf$/Inf\]\]/g' | sed 's/Inf/0/g' >> $out_file
        cat "$test_sce_dir/sinr_$sim.csv" | sed 's/^/, "sinr"\: \[/g' | sed 's/$/\]\}/g' | sed 's/Inf/401/g' | sed 's/nan/0/g' >> $out_file
    done
done



