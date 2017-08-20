

import os
import pandas as pd
import matplotlib.pyplot as plt

data_path = os.path.join("..", "findata")


def symbol_to_path(symbol, base_dir=data_path):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data_multiple_symbols(symbols, dates, addSPY=True, datatype='Adj Close'):

    # datatype = 'Open' 'High' 'Low' 'Close' 'Volume' 'Adj Close'
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                              parse_dates=True, usecols=['Date', datatype], na_values=['nan'])
        df_temp = df_temp.rename(columns={datatype: symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df .dropna(subset=["SPY"])
    df = df.sort_index(ascending=True)

    return df
    
    
def get_data_single_symbol(symbol, dates, 
                           datatypes=('Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')):

    # if 'Adj Close' not in datatypes:
    #    datatypes.append('Adj Close')
    
    df = pd.DataFrame(index=dates)
    df_read = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                          parse_dates=True, usecols=['Date'] + datatypes, na_values=['nan'])
    df = df.join(df_read)
    df = df.dropna()
    df = df.sort_index(ascending=True)
    
    return df


def get_data_all(symbols, dates, addSPY=True, 
                datatypes=('Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')):

    data = dict()
    for dt in datatypes:
        data[dt] = get_data_multiple_symbols(symbols, dates, addSPY=addSPY, datatype=dt)
    data = pd.Series(data)
    return data
    
    
def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price", kind = 'line', show = False):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12, kind = kind)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if show:
        plt.show()
