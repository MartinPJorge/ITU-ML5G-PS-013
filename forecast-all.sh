#!/bin/bash - 
#===============================================================================
#
#          FILE: forecast-all.sh
# 
#         USAGE: ./forecast-all.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 01/10/20 17:58
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error


if [ $# -ne 4 ]; then
    echo "specify input-files-directory out-files-directory TF-model-dir predictions-directory"
    exit 1
fi

in_dir=$1 # input-node-files-test/*
out_dir=$2
model_dir=$3
pred_dir=$4

for test_ in `ls -d $in_dir`; do
    echo "Test_=$test_"
    test_num=`echo $test_ | cut -d_ -f2`
    mkdir -p "$pred_dir/test_$test_num"

    for deployment in `ls $test_`; do
        deployment_num=`echo $deployment | cut -d_ -f6 | cut -d. -f1`
        echo "deployment_num=$deployment_num"

        # Create temporal directory with deployment files
        mkdir -p "/tmp/$test_"
        cp "$test_/$deployment" "/tmp/$test_"
        mkdir "/tmp/$out_dir"
        cp $out_dir"/sim_output_nodes_test_sce"$test_num"_deployment_"$deployment_num".json" "/tmp/$out_dir"

        # Trigger the forecasting
        new_dataset="/tmp/sc$test_num-dep$deployment_num.csv"
        python3 gossip.py 50 --new_dataset $new_dataset\
            --input_dir "/tmp/$test_" --parsed_output_dir "/tmp/$out_dir"
        solution_csv="$pred_dir/test_$test_num/all_throughput_$deployment_num.csv"
        echo "generating $solution_csv"
        python3 gossip.py 50 --dataset $new_dataset --model $model_dir > $solution_csv

        # create both AP and stations files
        sta_csv="$pred_dir/test_$test_num/stas_throughput_$deployment_num.csv"
        cat $solution_csv | grep STA_ | cut -d' ' -f3 | tr '\n' ',' | sed 's/\([0-9]\),$/\1\n/g' > $sta_csv
        aps_csv="$pred_dir/test_$test_num/throughput_$deployment_num.csv"
        cat $solution_csv | grep -e "^[A-Z] " | cut -d' ' -f3 | tr '\n' ',' | sed 's/\([0-9]\),$/\1\n/g' > $aps_csv

        rm -rf "/tmp/$test_"
        rm -rf "/tmp/$out_dir"
    done
done


