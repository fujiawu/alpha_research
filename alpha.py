
import numpy as np
import pandas as pd


def get_pct_ret(df):

    # df has to be a dataframe
    ret = df.copy()
    ret[1:] = df[1:]/df[:-1].values - 1
    ret = ret[1:]
    
    return ret


def get_abs_ret(df):
    # df has to be a dataframe
    ret = df.copy()
    ret[1:] = df[1:] - df[:-1].values
    ret = ret[1:]

    return ret


def alpha001(dfs):

    df = dfs['Adj Close']
    ret = get_pct_ret(df)

    win = 20
    ret[ret < 0] = ret.rolling(window=win).std()
    ret = ret[win-1:]
    ret1 = ret.copy()
    ret **= 2

    win = 5
    argmax = ret.rolling(window=win).apply(np.argmax)+1
    argmax = argmax[win-1:]
    alpha = argmax.rank(axis=1,pct=True)

    return alpha, ret1, argmax






    
    

    
    
    