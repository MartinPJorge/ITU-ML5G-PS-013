# ITU-ML5G-PS-013
This repository contains the solution of the ML 5G contest organized by ITU:
[https://www.itu.int/en/ITU-T/AI/challenge/2020/Pages/default.aspx](https://www.itu.int/en/ITU-T/AI/challenge/2020/Pages/default.aspx)

Particularly, it corresponds to problem statement 13. Participants have to
forecast the throughput of BSs and STAs in a 802.11 deployment:
[https://www.upf.edu/web/wnrg/ai_challenge](https://www.upf.edu/web/wnrg/ai_challenge)

![UPF image with routers and mobiles](img/challenge-image.png)

## Dataset
This repository already contains the dataset provided at:
[https://zenodo.org/record/3879458#.XwbRE9HtZPD](https://zenodo.org/record/3879458#.XwbRE9HtZPD)

 * `output-simulator`: contains the output files of the komodor simulator;
 * `input-node-files`: contains the CSVs of the different scenarios;
 * `output-simulator-parsed`: contains the parsed output files in a JSON format;

## Processing procedure
By running
```bash
./extract-outputs.sh output-simulator-parsed/
```
we parse the TXT files under `output-simulator` and store in a JSON the output
of each scenario.

During the parsing of the data, we encountered the following errors:
 * `output-simulator/script_output_sce1b.txt`: scenario 028 misses the RSSI data of x2 STAs. Thus, we fill it with the last throughput value;
 * `output-simulator/script_output_sce1a.txt`: scenario 014 misses the RSSI data of x2 STAs. Thus, we fill it with the last throughput value;
 * `output-simulator/script_output_sce1c.txt`: scenario 024 misses the RSSI data of x2 STAs. Thus, we fill it with the last throughput value;

The refered files are sanitized as indicated in this repository.


# Gossip
The `gossip.py` solution creates a dataset `gossip-dataset.csv` with
per-STA information. Each row corresponds to a STA, and the dataset is created
using all STAs present in the different scenarios.

The columns present are the following (as idx is the STA identifier):

| field | description |
|-------|-------------|
| primary_channel_neighs | TODO |
| primary_channel_0 | TODO |
| primary_channel_1 | TODO |
| primary_channel_2 | TODO |
| primary_channel_3 | TODO |
| primary_channel_4 | TODO |
| primary_channel_5 | TODO |
| primary_channel_6 | TODO |
| primary_channel_7 | TODO |
| allowed_channel_0 | TODO |
| allowed_channel_1 | TODO |
| allowed_channel_2 | TODO |
| allowed_channel_3 | TODO |
| allowed_channel_4 | TODO |
| allowed_channel_5 | TODO |
| allowed_channel_6 | TODO |
| allowed_channel_7 | TODO |
| rssi | TODO |
| q1_rssi | TODO |
| q2_rssi | TODO |
| q3_rssi | TODO |
| q4_rssi | TODO |
| agg_interference | TODO |
| channel_0_interference | TODO |
| channel_1_interference | TODO |
| channel_2_interference | TODO |
| channel_3_interference | TODO |
| channel_4_interference | TODO |
| channel_5_interference | TODO |
| channel_6_interference | TODO |
| channel_7_interference | TODO |
| throughput | TODO |
