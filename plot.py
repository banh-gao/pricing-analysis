import argparse
import pandas as pd
from os.path import basename
import matplotlib.pyplot as plt
from itertools import cycle
from scipy import interpolate

parser = argparse.ArgumentParser(description='Plot results')
parser.add_argument('results', type=str, nargs='?',
                    help='The aggregated result file')

args = parser.parse_args()

data = pd.DataFrame()

fig, ax = plt.subplots()
labels = []
df = pd.read_pickle(args.results)

lines = [":","-.","--","-"]
linecycler = cycle(lines)

for label, grp in df.groupby('scarcity'):
    grp = grp.sort_values(by=['utilization'])
    ax = grp.plot(ax=ax, kind='line', x='utilization', y='utility', linestyle=next(linecycler), linewidth=0.8)
    labels.append("scarcity=%s" % label)

    ax.fill_between(grp['utilization'], grp['utility'], 0, alpha=0.2, color='grey', linewidth=0)

    prev = grp

lines, _ = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='best')
plt.ylim(0,10)

fig.savefig('welfare.pdf')
