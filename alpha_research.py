import findata
import pandas as pd
import alpha
import numpy as np
import matplotlib.pyplot as plt

# read data
start_date = '2011-09-15'
end_date = '2011-12-31'
dates = pd.date_range(start_date, end_date)
symbols = ['SPY']
dfs = findata.get_data_all(symbols, dates)
df = dfs['Adj Close']

# create a normal time series with same sigma as SPY
normal = df['SPY'].copy()
val = normal.values
sigma = alpha.get_abs_ret(df)['SPY'].std()
for i in range(1, len(val)):
    val[i] = max(np.random.normal(val[i-1],sigma), 0)
df['NOM'] = normal

# create another normal time series
normal = df['SPY'].copy()
val = normal.values
sigma = alpha.get_abs_ret(df)['SPY'].std()*2
for i in range(1, len(val)):
    val[i] = max(np.random.normal(val[i-1],sigma), 0)
df['NOM2'] = normal


# create time series with momentum
momentum = df['SPY'].copy()
val = momentum.values
sigma = alpha.get_abs_ret(df)['SPY'].std()
for i in range(1, len(val)):
    inc = 2 * ( i % 5 - 2.5 ) / 2.5
    val[i] = val[i-1] + inc*sigma
df['MOM'] = momentum

# drop some columns computing alpha
df.drop('SPY', 1, inplace = True)
df.drop('NOM2', 1, inplace = True)

# calculate relative return
ret = alpha.get_pct_ret(df)

# compute alpha
alpha, ret1, argmax = alpha.alpha001(dfs)

# drop some columsn for plotting
alpha.drop('NOM', 1, inplace = True)
# ret1.drop('NOM', 1, inplace = True)
# argmax.drop('NOM', 1, inplace = True)
# ret.drop('NOM', 1, inplace = True)

# add return plots
ret_plot = ret.copy()
ret_plot.drop('NOM', 1, inplace = True)
ret_plot.drop('NOM', 1, inplace = True)
ret_plot['ret'] = ret['MOM']
ret_plot['ret1'] = ret1['MOM']

# plot
findata.plot_data(ret_plot, kind='line', title = 'alpha')
findata.plot_data(alpha, kind='line', title = 'alpha')
findata.plot_data(argmax, kind='line', title = 'argmax')
plt.show()


# plot kind: line, bar, hist, hexbin, barh, box, kde, density, area, pie, scatter


