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
import seaborn as sns; sns.set()

def readMT4data(filename, noOfLines):

    df = pd.read_csv(filename, delimiter=";", header=None)
    if (noOfLines < df.shape[0]):
        df = df[-noOfLines:] #get the latest number of lines specified
    
    df[0] = [datetime.datetime.fromtimestamp(
            int(d/1000)
        ).strftime('%Y-%m-%d %H:%M:%S') for d in df[0]]
    df.columns = ['time','h','l','o','c','v']
    
    df = df.assign(range=df.h-df.l) #calculate range per period
    df = df.assign(tPrice = (df.h + df.l + df.c) / 3) #calculate typical price
    
    return df;

def readInvData(filename, noOfLines=1000000): #Function to read Investing.com data
    df = pd.read_csv(filename, delimiter=";", header=None)
    
    if (noOfLines < df.shape[0]):
        df = df[:noOfLines] #get the latest number of lines specified
    df = df.reindex(index=df.index[::-1])
    df.reset_index(drop=True,inplace=True)
#    df[0] = [datetime.datetime.fromtimestamp(
#            int(d/1000)
#        ).strftime('%Y-%m-%d %H:%M:%S') for d in df[0]]
    
    df[0] = [datetime.datetime.strptime(d,'%b %d, %Y') for d in df[0]]
    
    df.columns = ['time','c','o','h','l']
    
    df = df.assign(range=df.h-df.l) #calculate range per period
    df = df.assign(tPrice = (df.h + df.l + df.c) / 3) #calculate typical price
    
    return df;

def readBTCdata(filename, noOfLines=1000000): #Function to read bitcoincharts.com
    df = pd.read_csv(filename, delimiter=";", header=None)
    
    if (noOfLines < df.shape[0]):
        df = df[:noOfLines] #get the latest number of lines specified
#    df[0] = [datetime.datetime.fromtimestamp(
#            int(d/1000)
#        ).strftime('%Y-%m-%d %H:%M:%S') for d in df[0]]
    
    df[0] = [datetime.datetime.strptime(d, "%d.%m.%Y %H:%M") for d in df[0]]
    
    df.columns = ['time','o','h','l','c','vBTC','vUSD','tPrice']
    # Timestamp	Open	High	Low	Close	Volume (BTC)	Volume (Currency)	Weighted Price
    
    df = df.assign(range=df.h-df.l) #calculate range per period
    
    
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

def plotHeatmap(results):
    heatmapdata = results.groupby(['histSize','patternLen']).sum().unstack('patternLen')
    fig, ax = plt.subplots(figsize=(results.shape[0],5)) 
    sns.heatmap(heatmapdata, annot=True, square=True, cmap = 'RdYlGn', center = 0.5, cbar = False)

def plotPerfHeatmap(modelPerf):
    df = modelPerf.pivot(index='patternLen', columns='histSize', values = 'perf')
    sns.heatmap(df, annot=True, square=True, cmap = 'RdYlGn', center = 0.5, cbar = False)
    


