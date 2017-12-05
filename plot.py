import argparse
import pandas as pd
from os.path import basename
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Plot results')
parser.add_argument('setup_results', type=str, nargs='+',
                    help='The aggregated result files')

args = parser.parse_args()

data = pd.DataFrame()

fig, ax = plt.subplots()
labels = []
for filename in args.setup_results:
    setup = basename(filename).strip('utilities_').rstrip('.pkl')
    grp = pd.read_pickle(filename)
    ax = grp.plot(ax=ax, kind='line', x='max_size', y='utility')
    labels.append(setup)

lines, _ = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='best')

fig.savefig('welfare.pdf')
