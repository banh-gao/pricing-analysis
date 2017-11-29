import glob
import pandas as pd
from os.path import basename

PARAMS = ['min_size', 'max_size', 'seed']

# splits the name of an output file by _ and extracts the values of simulation parameters
def get_params(filename):
    params = basename(filename).rstrip('.csv').split("_")[1:]
    out = {}
    for i in range(len(params)):
        out[PARAMS[i]] = params[i]
    return out


#Load Data
data_files='simulator/*.csv'

data = pd.DataFrame()

for filename in glob.glob(data_files):
    df = pd.read_csv(filename)
    params = get_params(filename)
    for name, val in params.items():
        df[name] = val

    data = data.append(df, ignore_index=True)

# Count acceptance rate
def acceptance(data):
    acceptance = data.loc[(data == 1)].count() / float(data.count())
    return acceptance

# Acceptance rate by size
bysize = data.groupby(['min_size', 'max_size'])
acceptance = bysize['accepted'].agg({ 'acceptance': acceptance })

fig = acceptance.plot().get_figure()
fig.savefig('acceptance.pdf')
