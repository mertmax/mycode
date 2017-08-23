# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:28:10 2017

@author: Efe
"""
import Utils 
import PatternDistribution as pattern

import pandas as pd

def surfacePatternDistribution(data):
    results = pd.DataFrame()
    for histSize in range(10,121,20):
        for patternLen in range(2,10,1):
            e = pattern.test(data,histSize = histSize, testSize = 50, patternLen = patternLen )
            ptr = e.log[e.log.pnl>0].shape[0]/e.log.shape[0]
            print("History: " + str(histSize) +
                  " Pattern Lenght: " + str(patternLen)+ 
                  " Profitable trade ratio " + str(ptr))
            new_result = pd.DataFrame([[histSize,patternLen,ptr]],columns = ["histSize","patternLen","ptr"])
            results = results.append(new_result)
    Utils.plot3d(results)

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

datafile  = "USDTRY-1440-HLOC-lag0-2017.08.08.csv"
histSize = 500
data = Utils.readMT4data(datafile, 99999)

results =surfacePatternDistribution(data)

#e = pattern.test(e,data,histSize, testSize = 50, patternLen = 5 )
#e.reportLog()



