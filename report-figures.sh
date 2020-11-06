## 
## # Create the TRAIN dataset
## cp -R input-node-files-v4 /tmp/input-node-files-v4-train
## for di in `ls -d /tmp/input-node-files-v4-train/*`; do
##     rm $di/*0{8,9}*
## done
## cp -R output-simulator-v4-parsed /tmp/output-simulator-v4-parsed-train
## rm /tmp/output-simulator-v4-parsed-train/*0{8,9}*
## python3 gossip.py 50 \
##     --new_dataset /tmp/gossip-dataset-v4-train.csv\
##     --input_dir /tmp/input-node-files-v4-train\
##     --parsed_output_dir /tmp/output-simulator-v4-parsed-train
## 
## python3 gossip.py 50 \
##     --dataset /tmp/gossip-dataset-v4-train.csv\
##     --model /tmp/gossip-trained-model\
##     --train --episodes 100


# Create the TEST dataset
rm -r /tmp/input-node-files-v4-test
cp -R input-node-files-v4 /tmp/input-node-files-v4-test
for di in `ls -d /tmp/input-node-files-v4-test/*`; do
    rm $di/*0{0,1,2,3,4,5,6,7}*
done
rm -r /tmp/output-simulator-v4-parsed-test
cp -R output-simulator-v4-parsed /tmp/output-simulator-v4-parsed-test
rm /tmp/output-simulator-v4-parsed-test/*0{0,1,2,3,4,5,6,7}*
rm /tmp/gossip-dataset-v4-test.csv
python3 gossip.py 50 \
    --new_dataset /tmp/gossip-dataset-v4-test.csv\
    --input_dir /tmp/input-node-files-v4-test\
    --parsed_output_dir /tmp/output-simulator-v4-parsed-test

# Create a dataset for 1 deployment of sce{1,2}{a,b,c}
for sc in `echo sce1a sce1b sce1c sce2a sce2b sce2c`; do
    rm -r /tmp/$sc-input-v4-test/$sc
    mkdir -p /tmp/$sc-input-v4-test/$sc
    cp /tmp/input-node-files-v4-test/$sc/*dep*080* /tmp/$sc-input-v4-test/$sc

    rm -r /tmp/$sc-output-v4-test/
    mkdir -p /tmp/$sc-output-v4-test/
    cp /tmp/output-simulator-v4-parsed-test/*dep*080* /tmp/$sc-output-v4-test/

    # Create the single deployment dataset
    echo -e "\n\n\nScenario $sc dataset creation\n\n\n"
    rm /tmp/$sc-gossip-dataset-v4-test.csv
    python3 gossip.py 50 --new_dataset /tmp/$sc-gossip-dataset-v4-test.csv --input_dir /tmp/$sc-input-v4-test --parsed_output_dir /tmp/$sc-output-v4-test

    # Derive results for the single deployment
    echo -e "\n\n\nScenario $sc NN execution\n\n\n"
    rm /tmp/$sc-dep080-results.csv
    python3 gossip.py 100 --dataset /tmp/$sc-gossip-dataset-v4-test.csv --model /tmp/gossip-trained-model > /tmp/$sc-dep080-results.csv

    # Derive APs and STAs CSVs
    echo -e "\n\n\nScenario $sc deployment 80 CSVs\n\n\n"
    grep "^STA" /tmp/$sc-dep080-results.csv | sed 's/\./,/g' |\
        sort -n -k2 > /tmp/sta-$sc-dep080-results.csv
    echo "AP real Gossip" > /tmp/aps-$sc-dep080-results.csv
    grep "^[A-Z] " /tmp/$sc-dep080-results.csv  | sed 's/\./,/g' |\
        sort -n -k2 >> /tmp/aps-$sc-dep080-results.csv
done



