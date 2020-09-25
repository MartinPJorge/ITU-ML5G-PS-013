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

if [ $# -ne 3 ]; then
    echo "specify in-directory out-directory v4"
    exit 1
fi

in_dir=$1
out_dir=$2
is_v4=$3


for f in `ls $in_dir`; do
    for l in `grep -n "KOMONDOR" "$in_dir/$f" | grep -oE "^[0-9]+"`; do

        # scenario 1 has 16|17 lines per scenario
        aps=12
        if [[ $is_v4 -gt 0 ]]; then
            tail_l=17;
        else
            tail_l=16
        fi

        # scenario 2 has 12|13 lines per scenario
        if [[ `echo $f | grep "sce2"` ]]; then
            aps=8
            if [[ $is_v4 -gt 0 ]]; then
                tail_l=13 
            else
                tail_l=12
            fi
        fi

        tail --lines=+$l "$in_dir/$f" | head -n$tail_l &> /tmp/sc.txt
    
        # Obtain the file name for the scenario
        sc_name=`head -n1 /tmp/sc.txt | grep -oE "[a-z0-9_]+\.csv"`
        sc_name=`echo $sc_name | sed 's/input/output/g' | sed 's/csv/json/g'`
        echo $sc_name
    
        throughput=`tail --lines=+2 /tmp/sc.txt | head -n1 | sed 's/{/[/g' | sed 's/}/]/g'`
        rssi=`tail --lines=+4 /tmp/sc.txt | head -n1 | sed 's/{/[/g' | sed 's/}/]/g' | sed 's/Inf/0/g'`
        interf_map=`tail --lines=+5 /tmp/sc.txt | head -n$aps | sed 's/{/[/g' | sed 's/}/];/g' | sed 's/^/[/g' | sed 's/;/],/g' | sed 's/Inf/0/g' | sed 's/]],/]]/g'`
        sinr=`tail --lines=+$(( 5 + aps )) /tmp/sc.txt | head -n1 | sed 's/{/[/g' | sed 's/}/]/g' | sed 's/Inf/401/g' | sed 's/nan/0/g'`

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
        echo "," >> "$out_dir/$sc_name"
        #
        echo '  "sinr": ' >> "$out_dir/$sc_name"
        echo $sinr>> "$out_dir/$sc_name"
        echo "}" >> "$out_dir/$sc_name"
    done
done



