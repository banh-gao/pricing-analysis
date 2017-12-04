import argparse
import pandas as pd
import numpy as np
from os.path import basename

PARAMS = ['min_size', 'max_size', 'seed']

# splits the name of an output file by _ and extracts the values of simulation parameters
def get_params(filename):
    params = basename(filename).rstrip('.csv').split("_")[1:]
    out = {}
    for i in range(len(params)):
        out[PARAMS[i]] = params[i]
    return out

# Calculate user and provider utilities
def net_utility(row):
    if row.accepted == 1:
        return row.offer
    else:
        return 0

parser = argparse.ArgumentParser(description='Process simulation data.')
parser.add_argument('in_files', type=str, nargs='+',
                    help='The data input files')

args = parser.parse_args()

#Load Data
data = pd.DataFrame()
for filename in args.in_files:
    df = pd.read_csv(filename)
    params = get_params(filename)
    for name, val in params.items():
        df[name] = val
    data = data.append(df, ignore_index=True)

# Acceptance rate by size
data['utility'] = data.apply(net_utility, axis=1)

bysize = data.groupby(['max_size'])
bysize = bysize.agg({'utility': np.sum})
print bysize
fig = bysize.plot().get_figure()
fig.savefig('acceptance.pdf')
