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

for f in `ls output-simulator-parsed/`; do n=`grep -n "throu" output-simulator-parsed/$f | cut -d':' -f1`; tail --lines=+$(( n + 1 )) output-simulator-parsed/$f | head -n1 | grep -oE "[0-9]+\.[0-9]+" | head -n1; done | sort -n


