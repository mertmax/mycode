# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:44:27 2017

Contains utility functions for data series analysis.

@author: Efe
"""
import datetime
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

def readMT4data(filename, noOfLines):

    df = pd.read_csv(filename, delimiter=";", header=None)
    if (noOfLines < df.shape[0]):
        df = df[-noOfLines:] #get the latest number of lines specified
    
    df[0] = [datetime.datetime.fromtimestamp(
            int(d/1000)
        ).strftime('%Y-%m-%d %H:%M:%S') for d in df[0]]
    df.columns = ['time','h','l','o','c','v']
    return df;

def plot3d(results):
    X = results.histSize
    Y = results.patternLen
    Z = results.ptr
    fig = plt.figure(figsize=(20,10))
    ax = fig.gca(projection='3d')
    ax.view_init(90, 0)
    ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True,cmap = cm.coolwarm,vmin=0.3)
    #fig.colorbar(ax)
    plt.show()



