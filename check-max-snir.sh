#!/bin/bash - 
#===============================================================================
#
#          FILE: check-max-throuput-1st-ap.sh
# 
#         USAGE: ./check-max-throuput-1st-ap.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 10/07/20 10:45
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

echo "Top 10 SINRs"
for f in `ls -d output-simulator-v4/*`; do
    for sim_line in `grep -n "KOMO" $f | cut -d':' -f1`; do
        sinrs=`tail --lines=+$(( sim_line + 1 )) $f | head -n1`
        for sinr in `echo $sinrs | sed -e 's/,/ /g' | sed -e 's/[\{\}]//g'`; do
            echo $sinr
        done
    done
done | sort -nur | head -n10


