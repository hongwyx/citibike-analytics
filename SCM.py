import pandas as pd
import numpy as np
import seaborn as sns


def synth_data(df, predictors, event, target, ):
	tdf = df.groupby(predictors+[event])[target].agg(['count', 'sum']).reset_index()
	cr = calc_ratio(tdf[predictors+[event]+['count']], predictors, event)
	tdf = tdf.merge(cr[predictors+['ratio']], left_on=predictors, right_on=predictors, how ='right')
	tdf['synth'] = np.where(tdf[event] == 0, tdf['sum']*tdf['ratio'], tdf['sum'])
	return tdf


def calc_ratio(tdf, predictors, event):
	cr = tdf.pivot_table(index=predictors, columns=event, values='count').reset_index().dropna()
	cr['ratio'] = cr[1]/cr[0]
	return cr

def calc_impact(df, predictors, event, target,):
    tdf = synth_data(df, predictors, event, target,)
    return 1- tdf[tdf[event] == 1]['sum'].sum()/tdf[tdf[event] == 0]['sum'].sum()

def plot(df, variable_bin, targets, normalize = False, plot_kind = 'bar'):
	sns.set_style("whitegrid")
	if normalize:
		df.groupby([variable_bin])[targets].mean().apply(lambda x: x/x.sum()).plot(kind = plot_kind, rot = 30)
	else:
		df.groupby([variable_bin])[targets].mean().plot(kind = plot_kind, rot = 30)
	return plt.gca()



