import sys
import os
import argparse
import pandas as pd
import numpy as np
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('batch', help="batch size ", type=int,
                        default=30)
    parser.add_argument('--train', help="specify training",
                        action='store_true')
    parser.add_argument('--dataset', help="path to csv with build dataset",
                        type=str)
    parser.add_argument('--new_dataset', help="path to csv with new dataset",
                        type=str)
    parser.add_argument('--test', help="specify testing",
                        action='store_true')
    parser.add_argument('--model', help="path to NN model",
                        type=str)
    parser.add_argument('--test-csvs', help="sce1.csv|sce2.csv",
                        action='store_true')
    args = parser.parse_args()


    # Create and store the dataset if it is not created
    if not args.dataset:
        if not args.new_dataset:
            print('Please specify the new dataset path')
            sys.exit(1)

        sta_rows = {
                    # node_code+scenario_name: {
                    #    #neighbors_in_channel: #neighbors
                    #
                    #    primary_channel_0: 0|1,
                    #        ...
                    #    primary_channel_7: 0|1,
                    #
                    #    allowed_channel_0: 0|1,
                    #        ...
                    #    allowed_channel_7: 0|1,
                    #
                    #    rssi: -30dB
                    #
                    #    q1_rssi: np.quantile(ap_rssis, 0.25)
                    #    q2_rssi: np.quantile(ap_rssis, 0.5)
                    #    q3_rssi: np.quantile(ap_rssis, 0.75)
                    #    q4_rssi: np.quantile(ap_rssis, 1)
                    #
                    #    agg_interference: the overall interference of AP
                    #
                    #    channel_0_interference: -23dB
                    #    channel_1_interference: -23dB
                    #    channel_2_interference: -23dB
                    #    channel_3_interference: -23dB
                    #    channel_4_interference: -23dB
                    #    channel_5_interference: -23dB
                    #    channel_6_interference: -23dB
                    #    channel_7_interference: -23dB
                    # }
                }

        for subdir, dirs, files in os.walk('input-node-files'):
            for file in files:
                filepath = subdir + os.sep + file

                # Read the scenario input
                print(f'reading csv {filepath}')
                scenario_in = pd.read_csv(filepath, sep=';')

                # Read the associated output
                fp_out = 'output-simulator-parsed/' +\
                        file.replace('input',
                                     'sim_output').replace('csv', 'json')
                print(f'reading {fp_out}')
                with open(fp_out, 'r') as f:
                    scenario_out = json.load(f)


                # Obtain APs, and getthe interference map idx
                aps = scenario_in[scenario_in['node_type'] == 0]
                map_idx = {
                    ap_idx: map_idx
                    for (ap_idx, ap_row), map_idx in zip(aps.iterrows(),
                                                     range(len(aps)))
                }

                # Iterate over each AP
                for ap_idx, ap_row in aps.iterrows():
                    ap = ap_row['wlan_code']
                    stas = scenario_in[(scenario_in['node_type'] == 1) &\
                            (scenario_in['wlan_code'] == ap)]

                    # RSSI quantiles of the attached STAs
                    rssis = [scenario_out['rssi'][st_idx]\
                             for st_idx in stas.index]
                    q1_rssi = np.quantile(rssis, 0.25)
                    q2_rssi = np.quantile(rssis, 0.5)
                    q3_rssi = np.quantile(rssis, 0.75)
                    q4_rssi = np.quantile(rssis, 1)

                    # AP overall interference
                    agg_interference =\
                        sum(scenario_out['interference'][map_idx[ap_idx]])

                    # Per channel AP interference
                    other_aps = scenario_in[(scenario_in['node_type'] == 0) &\
                            (scenario_in['wlan_code'] != ap)]
                    per_channel_interference = [0 for _ in range(8)]
                    for o_ap_idx, o_ap_row in other_aps.iterrows():
                        for ch in range(ap_row['min_channel_allowed'],
                                ap_row['max_channel_allowed']):
                            if ch >= o_ap_row['min_channel_allowed'] and\
                                    ch <= o_ap_row['max_channel_allowed']:
                                per_channel_interference[ch] +=\
                                        scenario_out['interference'][
                                                map_idx[ap_idx]
                                                ][map_idx[o_ap_idx]]


                    ######################
                    # Iter over each STA #
                    ######################
                    for index, st_row in stas.iterrows():
                        st_key = file + '_' + st_row['node_code']
                        sta_rows[st_key] = {}

                        # Neighbor STAs in same primary_channel
                        sta_rows[st_key]['primary_channel_neighs'] =\
                                len(stas[stas['primary_channel'] ==\
                                        st_row['primary_channel']]) - 1

                        # STA primary channel vector
                        for ch in range(8):
                            sta_rows[st_key]['primary_channel_' + str(ch)] =\
                                    1 if st_row['primary_channel'] == ch else 0

                        # STA allowed channels vector - matches the AP ones
                        for ch in range(8):
                            if ch <= int(st_row['max_channel_allowed']) and\
                                    ch >= int(st_row['min_channel_allowed']):
                                sta_rows[st_key][
                                        'allowed_channel_' + str(ch)] = 1
                            else:
                                sta_rows[st_key][
                                        'allowed_channel_' + str(ch)] = 0

                        # The STA RSSI level
                        sta_rows[st_key]['rssi'] = scenario_out['rssi'][index]

                        # The RSSIs quantiles of neighboring nodes
                        sta_rows[st_key]['q1_rssi'] = q1_rssi
                        sta_rows[st_key]['q2_rssi'] = q2_rssi
                        sta_rows[st_key]['q3_rssi'] = q3_rssi
                        sta_rows[st_key]['q4_rssi'] = q4_rssi

                        # Aggregated interferences
                        sta_rows[st_key]['agg_interference'] = agg_interference

                        # Per channel AP interferences
                        for ch in range(8):
                            sta_rows[st_key][f'channel_{ch}_interference'] =\
                                    per_channel_interference[ch]

                        # STA throughput
                        sta_rows[st_key]['throughput'] =\
                                scenario_out['throughput'][index]

        # Create and store the data-set
        new_df = pd.DataFrame.from_dict(sta_rows, orient='index')
        print(f'saving the dataset in: {args.new_dataset}')
        new_df.to_csv(args.new_dataset)





