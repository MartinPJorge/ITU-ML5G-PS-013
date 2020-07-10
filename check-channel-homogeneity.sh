#!/bin/bash - 
#===============================================================================
#
#          FILE: check-channel-homogeneity.sh
# 
#         USAGE: ./check-channel-homogeneity.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 10/07/20 09:49
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

file="input-node-files/sce1a/input_nodes_sce1a_deployment_001.csv"

for file in `ls input-node-files/*/*`; do
    echo "Checking file $file"

    # Lines where APs start
    lns=()
    for l in `grep -n -E "AP_[A-Z]+;0" $file`; do
        lns+=(`echo $l | cut -d':' -f1`)
    done
    lns+=(`wc -l $file | cut -d' ' -f1`)
    
    
    for l in `seq 1 $(( ${#lns[@]} - 2 ))`; do
        used_channels=`tail --lines=+$(( ${lns[l]} + 1 )) $file | head -n$(( ${lns[l+1]} - ${lns[l]} )) | cut -d';' -f9 | sort -u`
    
        # If the AP has users selecting multiple primary channels
        if [ `echo $used_channels | wc -l` -ge 2 ]; then
            AP=`tail --lines=+${lns[l]} $file | head -n1 | cut -d';' -f1`
            echo "============="
            echo "in scenario $file, AP:$AP has users selecting these channels:"
            echo $used_channels
            echo "============="
        fi
    done

done

