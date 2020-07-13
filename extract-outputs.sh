#!/bin/bash - 
#===============================================================================
#
#          FILE: extract-outputs.sh
# 
#         USAGE: ./extract-outputs.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 09/07/20 16:58
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

if [ $# -ne 2 ]; then
    echo "specify in-directory out-directory"
    exit 1
fi

in_dir=$1
out_dir=$2


for f in `ls $in_dir`; do
    for l in `grep -n "KOMONDOR" "$in_dir/$f" | grep -oE "^[0-9]+"`; do

        tail_l=16 # scenario 1 has 16 lines per scenario
        if [[ `echo $f | grep "sce2"` ]]; then
            tail_l=12 # scenario 2 has 12 lines per scenario
        fi

        tail --lines=+$l "$in_dir/$f" | head -n$tail_l &> /tmp/sc.txt
    
        # Obtain the file name for the scenario
        sc_name=`head -n1 /tmp/sc.txt | grep -oE "[a-z0-9_]+\.csv"`
        sc_name=`echo $sc_name | sed 's/input/output/g' | sed 's/csv/json/g'`
        echo $sc_name
    
        throughput=`tail --lines=+2 /tmp/sc.txt | head -n1 | sed 's/{/[/g' | sed 's/}/]/g'`
        rssi=`tail --lines=+4 /tmp/sc.txt | head -n1 | sed 's/{/[/g' | sed 's/}/]/g' | sed 's/Inf/0/g'`
        interf_map=`tail --lines=+5 /tmp/sc.txt | sed 's/{/[/g' | sed 's/}/];/g' | sed 's/^/[/g' | sed 's/;/],/g' | sed 's/Inf/0/g' | sed 's/]],/]]/g'`

        # create the JSON with output data
        echo "{" >> "$out_dir/$sc_name"
        echo '  "throughput": ' >> "$out_dir/$sc_name"
        echo $throughput >> "$out_dir/$sc_name"
        echo "," >> "$out_dir/$sc_name"
        #
        echo '  "rssi": ' >> "$out_dir/$sc_name"
        echo $rssi>> "$out_dir/$sc_name"
        echo "," >> "$out_dir/$sc_name"
        #
        echo '  "interference": ' >> "$out_dir/$sc_name"
        echo $interf_map >> "$out_dir/$sc_name"
        echo "}" >> "$out_dir/$sc_name"
    done
done



