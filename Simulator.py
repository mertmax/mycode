# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:28:10 2017

@author: Efe
"""

import PatternDistribution as pattern
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def surfacePatternDistribution():
    results = pd.DataFrame()
    for histSize in range(500,501,1):
        for patternLen in range(4,5,1):
            e = pattern.test("USDTRY-1440-HLOC-lag0-2017.08.08.csv",-1270,histSize = histSize, testSize = 50, patternLen = patternLen )
            ptr = e.log[e.log.pnl>0].shape[0]/e.log.shape[0]
            print("History: " + str(histSize) +
                  " Pattern Lenght: " + str(patternLen)+ 
                  " Profitable trade ratio " + str(ptr))
            new_result = pd.DataFrame([[histSize,patternLen,ptr]],columns = ["histSize","patternLen","ptr"])
            results = results.append(new_result)
    threedee = plt.figure(figsize=(10, 10), dpi=80).gca(projection='3d')
    threedee.scatter(results.histSize,results.patternLen,results.ptr)
    return results

def runPatternDistribution(histSize,patternLen):
    e = pattern.test("USDTRY-1440-HLOC-lag0-2017.08.08.csv",-1270,histSize = histSize, testSize = 50, patternLen = patternLen )
    ptr = e.log[e.log.pnl>0].shape[0]/e.log.shape[0]
    ppt = e.log.pnl.sum() /e.log.shape[0]
    print("History: " + str(histSize) +
      " Pattern length: " + str(patternLen)+ 
      " Profitable trade ratio " + str(ptr)+
      " Avg. profit per trade " + str(ppt))
    return e.log

e = runPatternDistribution(500,4)