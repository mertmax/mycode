# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:44:27 2017

Contains utility functions for data series analysis.

@author: Efe
"""
import datetime
import pandas as pd

def readMT4data(filename):

    df = pd.read_csv(filename, delimiter=";", header=None)
    
    df[0] = [datetime.datetime.fromtimestamp(
            int(d/1000)
        ).strftime('%Y-%m-%d %H:%M:%S') for d in df[0]]
    df.columns = ['time','h','l','o','c','v']
    return df;

