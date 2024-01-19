import numpy as np
import pandas as pd

df = pd.read_csv("CSVs/output_250_15_3.csv")

def train_test_split(data, responses, frac=0.8, shuffle=True, rs=0):
	if isinstance(responses, list) == False:
		raise Exception("responses must be a list of column names")

	df = data.sample(frac=1, random_state=rs) if shuffle else data

	split_point = int(frac*len(df.index))
	train = df[:split_point]
	test = df[split_point:]

	train_X = train[train.columns[~train.columns.isin(responses)]]
	train_Y = train[responses]

	test_X = test[test.columns[~test.columns.isin(responses)]]
	test_Y = test[responses]

	return (train_X, train_Y, test_X, test_Y)

def batch(data, batches, responses, shuffle=True, rs=0):
	if isinstance(responses, list) == False:
		raise Exception("responses must be a list of column names")
	
	df = data.sample(frac=1, random_state=rs) if shuffle else data

	batch_size = int(len(df.index) / batches)
	split_points = [i * batch_size for i in range(batches)]
	split_points.append(len(df.index))

	groups = [df[split_points[i]:split_points[i+1]] for i in range(batches)]

	x_sets = [g[g.columns[~g.columns.isin(responses)]] for g in groups]
	y_sets = [g[responses] for g in groups]

	return (x_sets, y_sets)
