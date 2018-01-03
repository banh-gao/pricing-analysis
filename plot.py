import argparse
import pandas as pd
from os.path import basename
import matplotlib.pyplot as plt
from itertools import cycle
from scipy.interpolate import interp1d
from scipy import linspace

parser = argparse.ArgumentParser(description='Plot results')
parser.add_argument('results', type=str, nargs='?',
                    help='The aggregated result file')

args = parser.parse_args()

data = pd.DataFrame()

labels = []
df = pd.read_pickle(args.results)

lines = [":","-.","--","-"]
linecycler = cycle(lines)

plot_data = pd.DataFrame()

for label, grp in df.groupby('scarcity'):
    grp = grp.drop_duplicates(subset=['utilization']).sort_values(by=['utilization'])

    interp = interp1d(grp['utilization'], grp['utility'], kind='cubic')

    xnew = linspace(grp['utilization'].min(), grp['utilization'].max(),
                    num=100)

    plt.plot(xnew, interp(xnew) ,
             linestyle=next(linecycler), linewidth=0.8, label="scarcity=%s" % label)

    plt.fill_between(xnew, interp(xnew), 0, alpha=0.2, color='grey', linewidth=0.5)

    labels.append("scarcity=%s" % label)

plt.legend(loc='upper left')

plt.xlim(df['utilization'].min(), df['utilization'].max())
plt.xlabel('utilization')

plt.ylim(0, df['utility'].max() + 1)
plt.ylabel('unit price')

plt.savefig('welfare.pdf')
