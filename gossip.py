import re
import tensorflow as tf
import sys
import os
import argparse
import pandas as pd
import numpy as np
import json

# INPUT_DIR='input-node-files'
# OUT_PARSED_DIR='output-simulator-parsed'

# original set of columns to use
COLUMNS_0=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'allowed_channel_0', 'allowed_channel_1', 'allowed_channel_2',
        'allowed_channel_3', 'allowed_channel_4', 'allowed_channel_5',
        'allowed_channel_6', 'allowed_channel_7', 'rssi', 'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# Just without the quantile-rssi, and per-channel interference
COLUMNS_1=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'allowed_channel_0', 'allowed_channel_1', 'allowed_channel_2',
        'allowed_channel_3', 'allowed_channel_4', 'allowed_channel_5',
        'allowed_channel_6', 'allowed_channel_7', 'rssi',
        'agg_interference','throughput']

# Remove the primary channel info, and aggregated interference
COLUMNS_2=['primary_channel_neighs', 'allowed_channel_1', 'allowed_channel_2',
        'allowed_channel_3', 'allowed_channel_4', 'allowed_channel_5',
        'allowed_channel_6', 'allowed_channel_7', 'rssi', 'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# without the allowed channels
COLUMNS_3=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'rssi', 'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# without the allowed channels, and aggregated interference
COLUMNS_4=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'rssi', 'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# without the allowed channels, and the RSSI
COLUMNS_5=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# without the allowed channels, and q{3,4}_rssi
COLUMNS_6=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'rssi', 'q1_rssi', 'q2_rssi',
        'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

# without the allowed channels, and q{1,2}_rssi
COLUMNS_7=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'rssi', 'q3_rssi', 'q4_rssi',
        'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

#################################
# COLUMN COMBINATIONS WITH SINR #
#################################

COLUMNS_10=['primary_channel_neighs', 'primary_channel_0', 'primary_channel_1',
        'primary_channel_2', 'primary_channel_3', 'primary_channel_4',
        'primary_channel_5', 'primary_channel_6', 'primary_channel_7',
        'allowed_channel_0', 'allowed_channel_1', 'allowed_channel_2',
        'allowed_channel_3', 'allowed_channel_4', 'allowed_channel_5',
        'allowed_channel_6', 'allowed_channel_7', 
        'sinr','q1_sinr', 'q2_sinr', 'q3_sinr', 'q4_sinr',
        'rssi', 'q1_rssi', 'q2_rssi',
        'q3_rssi', 'q4_rssi', 'agg_interference', 'channel_0_interference',
        'channel_1_interference', 'channel_2_interference',
        'channel_3_interference', 'channel_4_interference',
        'channel_5_interference', 'channel_6_interference',
        'channel_7_interference', 'throughput']

COLUMNS=COLUMNS_0
LABEL=COLUMNS[-1]


if __name__ == '__main__':
    global INPUT_DIR, OUT_PARSED_DIR 
    parser = argparse.ArgumentParser()
    parser.add_argument('batch', help="batch size ", type=int,
                        default=30)
    parser.add_argument('--train', help="specify training",
                        action='store_true')
    parser.add_argument('--episodes', help="training episodes",
                        type=int)
    parser.add_argument('--dataset', help="path to csv with build dataset",
                        type=str)
    parser.add_argument('--new_dataset', help="path to csv with new dataset",
                        type=str)
    parser.add_argument('--input_dir', help="path to dir with input data",
                        type=str)
    parser.add_argument('--parsed_output_dir', help="path dir with parsed out",
                        type=str)
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
        if not args.input_dir or not args.parsed_output_dir:
            print('Please specify input and output directories')
        INPUT_DIR = args.input_dir
        OUT_PARSED_DIR = args.parsed_output_dir

        print('Creating the dataset')
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
                    #    sinr: -30dB
                    #
                    #    q1_sinr: np.quantile(ap_sinrs, 0.25)
                    #    q2_sinr: np.quantile(ap_sinrs, 0.5)
                    #    q3_sinr: np.quantile(ap_sinrs, 0.75)
                    #    q4_sinr: np.quantile(ap_sinrs, 1)
                    #
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
                    #
                    #    scenario: 'sce1b'
                    #    deployment: '099'
                    #    node_code: st_row['node_code']
                    #    wlan_code: st_row['wlan_code']
                    #    node_x: node x coordinate
                    #    node_y: node y coordinate
                    #    node_r: node z coordinate
                    #    ap_x: AP x coordinate
                    #    ap_y: AP y coordinate
                    #    ap_r: AP z coordinate
                    # }
                }

        for subdir, dirs, files in os.walk(INPUT_DIR):
            for file in files:
                filepath = subdir + os.sep + file

                # Read the scenario input
                print(f'reading csv {filepath}')
                scenario_in = pd.read_csv(filepath, sep=';')

                # Read the associated output
                fp_out = OUT_PARSED_DIR + '/' +\
                        file.replace('input',
                                     'sim_output').replace('csv', 'json')
                print(f'reading {fp_out}')
                with open(fp_out, 'r') as f:
                    scenario_out = json.load(f)

                # Obtain both the scenario and #deployment
                scenario = re.search(r'sce\d+[a-z]', file)[0]
                deployment = re.search(r'\d+\.csv', file)[0].split('.')[0]


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

                    # SNIR quantiles of the attached STAs
                    sinrs = [scenario_out['sinr'][st_idx]\
                             for st_idx in stas.index]
                    q1_sinr = np.quantile(sinrs, 0.25)
                    q2_sinr = np.quantile(sinrs, 0.5)
                    q3_sinr = np.quantile(sinrs, 0.75)
                    q4_sinr = np.quantile(sinrs, 1)

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
                        sta_rows[st_key] = {
                            'node_code': st_row['node_code'],
                            'wlan_code': st_row['wlan_code'],
                            'scenario': scenario,
                            'deployment': deployment,
                            'node_x': st_row['x(m)'],
                            'node_y': st_row['y(m)'],
                            'node_z': st_row['z(m)'],
                            'ap_x': ap_row['x(m)'],
                            'ap_y': ap_row['y(m)'],
                            'ap_z': ap_row['z(m)']
                        }

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

                        # The STA SINR level
                        sta_rows[st_key]['sinr'] = scenario_out['sinr'][index]

                        # The SINRs quantiles of neighboring nodes
                        sta_rows[st_key]['q1_sinr'] = q1_sinr
                        sta_rows[st_key]['q2_sinr'] = q2_sinr
                        sta_rows[st_key]['q3_sinr'] = q3_sinr
                        sta_rows[st_key]['q4_sinr'] = q4_sinr

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



    # Dataset created / read
    # Training selected
    if args.train:
        if not args.episodes:
            print('Please specify number of episodes')
            sys.exit(1)
        if not args.model:
            print('Please specify the path where the model will be stored')
            sys.exit(1)
        if not args.batch:
            print('Please specify the batch size for the training')
            sys.exit(1)



        # Create the NN model - 36.85 of loss
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.tanh,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.tanh),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 23.73 after 50 episodes, batch=32
        model = tf.keras.Sequential([
          tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu,
                                input_shape=(len(COLUMNS)-1,)),  # input shape required
          tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu),
          tf.keras.layers.Dense(1)
        ])

        # Loss of 24.03 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 32.1875 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(7, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   #tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 25.2731 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(5, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 32.5512 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.LayerNormalization(input_shape=(len(COLUMNS)-1,)),
        ##   tf.keras.layers.Dense(5, activation=tf.nn.relu
        ##                         ),  # input shape required
        ##   tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 38.3275 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(5, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.LayerNormalization(),
        ##   tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 23.5528 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(2*len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(2*len(COLUMNS)-1, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])


        # with COLUMNS_0
        # Loss of 23.3159 after 50 episodes, batch=32 - RMSprop
        # Loss of 23.0665 after 50 episodes, batch=32 - Adams
        # Loss of 35.8017 after 50 episodes, batch=32 - Adamgrad
        # with COLUMNS_1
        # Loss of 24.8166 after 50 episodes, batch=32 - RMSprop
        # Loss of 24.1164 after 50 episodes, batch=32 - Adams
        # with COLUMNS_2
        # Loss of 29.4542 after 50 episodes, batch=32 - Adams
        # with COLUMNS_3
        # Loss of 23.1211 after 50 episodes, batch=32 - Adams
        # with COLUMNS_4
        # Loss of 29.5364 after 50 episodes, batch=32 - Adams
        # with COLUMNS_5
        # Loss of 25.9326 adter 50 episodes - Adams
        # with COLUMNS_6
        # Loss of 23.1025 after 50 episodes, batch=32 - Adams
        # with COLUMNS_7
        # Loss of 23.5411 after 50 episodes, batch=32 - Adams
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(3*len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(3*len(COLUMNS)-1, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # COLUMNS_0
        # Loss of 23.1621 after 50 episodes, batch=32 - Adams
        # Loss of 23.9611 after 50 episodes, batch=32 - RMSprop
        # Loss of 23.1937 after 50 episodes, batch=50 - RMSprop
        # Loss of 23.5262 after 50 episodes, batch=100 - RMSprop
        model = tf.keras.Sequential([
          tf.keras.layers.Dense(5*len(COLUMNS)-1, activation=tf.nn.relu,
                                input_shape=(len(COLUMNS)-1,)),  # input shape required
          tf.keras.layers.Dense(5*len(COLUMNS)-1, activation=tf.nn.relu),
          tf.keras.layers.Dense(1)
        ])

        # Loss of 23.9577 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 23.7363 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dense(10, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(3, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Loss of 28.7471 after 50 episodes, batch=32
        ## model = tf.keras.Sequential([
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu,
        ##                         input_shape=(len(COLUMNS)-1,)),  # input shape required
        ##   tf.keras.layers.Dropout(.2),
        ##   tf.keras.layers.Dense(len(COLUMNS)-1, activation=tf.nn.relu),
        ##   tf.keras.layers.Dense(1)
        ## ])

        # Specify loss and gradient method
        model.compile(
            optimizer=tf.keras.optimizers.RMSprop(),  # Optimizer
            #optimizer=tf.keras.optimizers.Adam(),  # Optimizer
            #optimizer=tf.keras.optimizers.Adagrad(),  # Optimizer
            # Loss function to minimize
            loss=tf.keras.losses.MeanSquaredError(),
            # List of metrics to monitor
            metrics=[tf.keras.metrics.MeanSquaredError()],
        )


        train_dataset_fp = args.dataset if args.dataset else args.new_dataset
        df = pd.read_csv(train_dataset_fp)
        df = df[COLUMNS] # retain only interesting columns
        df = df.sample(frac=1) # shuffle the dataframe
        # 0.8-train, 0.2-test
        df_train = df.iloc[:, :int(0.8*len(df))]
        df_test = df.iloc[:, int(0.8*len(df)):]
        # 0.2 of train for validation
        df_val = df_train[int(-0.2*len(df_train)):]
        df_train = df_train[:int(-0.2*len(df_train))]

        

        # Fit the data
        history = model.fit(
            x=df_train.drop(columns=[LABEL]),
            y=df_train[LABEL],
            batch_size=args.batch,
            epochs=args.episodes,
            # We pass some validation for
            # monitoring validation loss and metrics
            # at the end of each epoch
            validation_data=(df_val.drop(columns=[LABEL]), df_val[LABEL]),
        )

    
        # Store the model
        print(f'Storing the trained model at: {args.model}')
        model.save(args.model)


    # Run forecasting
    else:
        if not args.model:
            print('Please specify the model to use')
            sys.exit(1)

        # Load the model
        model = tf.keras.models.load_model(args.model)

        # Load the dataset
        dataset_fp = args.dataset if args.dataset else args.new_dataset
        df = pd.read_csv(dataset_fp)
        df_nn = df[COLUMNS] # retain only interesting columns
        df_no_lab = df_nn.drop(columns=[LABEL])

        # Forecast the throughput
        forecast = model.predict(df_no_lab)
        forecast_df = df.copy()
        forecast_df['throughput'] = forecast

        print('===========================')
        print('= STA throughput forecast =')
        print('===========================')
        print('node_code real_throughput forecast_throughput')
        for idx, row in df.iterrows():
            forecast = forecast_df[forecast_df['node_code'] ==\
                    row['node_code']]['throughput'].values[0]
            print(f'{row["node_code"]} {row["throughput"]} {forecast}')

        # APs' forecasted throughput
        print('=================')
        print('= AP throughput =')
        print('=================')
        ap_forecast = forecast_df.groupby(['wlan_code']).sum()
        ap_real = df.groupby(['wlan_code']).sum()

        print('wlan_code real_throughput forecast_throughput')
        for wc_real, row in ap_real.iterrows():
            for wc_fore, row_f in ap_forecast.iterrows():
                if wc_real == wc_fore:
                    print(wc_real, row['throughput'], row_f['throughput'])



        



