import argparse
import pandas as pd
import numpy as np
from os.path import basename

PARAMS = ['scarcity']

# splits the name of an output file by _ and extracts the values of simulation parameters
def get_params(filename):
    params = basename(filename).rstrip('.csv').split("_")[1:]
    out = {}
    for i in range(len(params)):
        out[PARAMS[i]] = float(params[i])
    return out

parser = argparse.ArgumentParser(description='Process simulation data.')
parser.add_argument('in_files', type=str, nargs='+',
                    help='The data input files')

args = parser.parse_args()

#Load Data
df = pd.DataFrame()
for filename in args.in_files:
    csv = pd.read_csv(filename)

    params = get_params(filename)
    for name, val in params.items():
        csv[name] = val

    df = df.append(csv, ignore_index=True)

df = df[df.accepted == 1]

# Calculate utility of each deployment
df['utility'] = df.apply(lambda x : x.unit_price, axis=1)

df.to_pickle("./utilities.pkl")
