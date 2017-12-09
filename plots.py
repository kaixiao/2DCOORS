import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv

pickle_fn = 'good_results/compiled.pkl'

vals = pickle.load(open(pickle_fn, "rb"))

# Fixed number of points
fnp = vals[vals['num points'] == 2000]
fnp_small_box = fnp[fnp['box type'] == 'smallBoxes']
fnpsb_ds = fnp_small_box.sort_values(['data structure', 'memory size', 'block size'])
fnpsb_final = fnpsb_ds[['data structure', 'memory size', 'block size',
						'avg cell probes', 'std cell probes',
						'avg disk accesses', 'std disk accesses']]
fnpsb_final.to_csv('good_results/fnpsb.csv')
# fnp_small_box_csv = 'good_results/fnp_small_box.csv'
# with open(fnp_small_box_csv, 'w') as csvfile:
# 	fieldnames = ['memory size', 'block size', 'avg cell probes',
# 				'std cell probes', 'avg disk accesses', 'std disk accesses',
# 				'data structure']
# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 	writer.writeheader()
# 	rows_to_write = []

# 	# make chart of DS vs memory_config
# 	for ds in fnp_small_box['data structure'].unique():
# 		temp_df = fnp_small_box[fnp_small_box['data structure'] == ds]
# 		for i in range(len(temp_df)):
# 			row = temp_df.iloc[i]
# 			print(row['memory size'], row['block size'],
# 				row['avg cell probes'], row['std cell probes'],
# 				row['avg disk accesses'], row['std disk accesses'])
# 			rows_to_write.append({
# 				'memory size': row['memory size'],
# 				'block size': row['block size'],
# 				'avg cell probes': row['avg cell probes'],
# 				'std cell probes': row['std cell probes'],
# 				'avg disk accesses': row['avg disk accesses'],
# 				'std disk accesses': row['std disk accesses']
# 				})
# 		for row in rows_to_write:
# 			writer.writerow(row)

fnp_big_box = fnp[fnp['box type'] == 'bigBoxes']
fnpbb_ds = fnp_big_box.sort_values(['data structure', 'memory size', 'block size'])
fnpbb_final = fnpbb_ds[['data structure', 'memory size', 'block size',
						'avg cell probes', 'std cell probes',
						'avg disk accesses', 'std disk accesses']]
fnpbb_final.to_csv('good_results/fnpbb.csv')

# Fixed Memory config
fm = vals[(vals['block size'] == 8) & (vals['memory size'] == 32)]
fm_small_box = fm[fm['box type'] == 'smallBoxes']
fmsb_ds = fm_small_box.sort_values(['data structure', 'num points'])
fmsb_final = fmsb_ds[['data structure', 'num points',
						'avg cell probes', 'std cell probes',
						'avg disk accesses', 'std disk accesses']]
fmsb_final.to_csv('good_results/fmsb.csv')

fm_big_box = fm[fm['box type'] == 'bigBoxes']
fmbb_ds = fm_big_box.sort_values(['data structure', 'num points'])
fmbb_final = fmbb_ds[['data structure', 'num points',
						'avg cell probes', 'std cell probes',
						'avg disk accesses', 'std disk accesses']]
fmbb_final.to_csv('good_results/fmbb.csv')

# for fixed memory, how does increasing points compare?
# 	small vs big queries
# 	graphical representation (for each DS)
