import pickle
import os
import pandas as pd

pickle_dir = 'good_results/'

all_pkls = []
for fn in os.listdir(pickle_dir):
	if fn[-3:] == 'pkl':
		true_fn = os.path.join(pickle_dir, fn)
		all_pkls.append(pickle.load(open(true_fn, "rb")))

df = pd.concat(all_pkls)
df['avg disk accesses'] = df['num disk accesses']/df['num queries']
df['avg cell probes'] = df['num cell probes']/df['num queries']


group_by_keys = ['box type', 'data structure', 
				'block size', 'memory size', 'num points']

grouped_df=df.groupby(group_by_keys)


pd.set_option('display.max_rows', None) 

d = dict()
for key in group_by_keys:
	d[key] = []
d['avg disk accesses'] = []
d['std disk accesses'] = []
d['avg cell probes'] = []
d['std cell probes'] = []

for k in grouped_df.groups.keys():
	group = grouped_df.get_group(k)
	avg_disk_accesses = group['avg disk accesses'].mean()
	std_disk_accesses = group['avg disk accesses'].std()
	avg_cell_probes = group['avg cell probes'].mean()
	std_cell_probes = group['avg cell probes'].std()
	for i in range(len(group_by_keys)):
		key = group_by_keys[i]
		d[key].append(k[i])
	d['avg disk accesses'].append(avg_disk_accesses)
	d['std disk accesses'].append(std_disk_accesses)
	d['avg cell probes'].append(avg_cell_probes)
	d['std cell probes'].append(std_cell_probes)

compiled_df = pd.DataFrame(data=d)

compiled_df.to_csv(os.path.join(pickle_dir, 'compiled.csv'))
compiled_df.to_pickle(os.path.join(pickle_dir, 'compiled.pkl'))

# grouped_df['avg disk accesses'].mean()
# grouped_df['avg disk accesses'].std()
# grouped_df['avg cell probes'].mean()
# grouped_df['avg cell probes'].std()

