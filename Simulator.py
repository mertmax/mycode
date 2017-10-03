# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:28:10 2017

@author: Efe
"""
import Utils 
import PatternDistribution as pattern

import pandas as pd

def testLimitParams(allData,slLevels, tpLevels):
    testRes = pd.DataFrame()
    newRes = evalPatternDistribution(data,histRange, patternLenRange, slLevels = slLevels, tpLevels = tpLevels )
    testRes.append(newRes)
    testRes.reset_index(drop=True, inplace=True)
    return testRes

def evaluatePerfomance(cvSet,histRange,patternLenRange):
    perfomances = pd.DataFrame();
    for histSize in histRange:
        for patternLen in patternLenRange:
            perf = cvSet.loc[cvSet.patternLen==patternLen].loc[cvSet.histSize==histSize].ptr.mean()
            perfomances = perfomances.append(pd.DataFrame([[histSize, patternLen, perf]],columns = ["histSize", "patternLen", "perf"]))
    return perfomances

def crossValidatePatternDistribution(allData,histRange, patternLenRange,cvFold):
    cvSet = pd.DataFrame()
    dataSize = int((allData.shape[0] - allData.shape[0]%cvFold)/cvFold)
    for i in range(0,cvFold,1):
        data = allData[i*dataSize:(i+1)*dataSize]
        #result = evalPatternDistribution(data,histRange, patternLenRange)
        newCv = evalPatternDistribution(data,histRange, patternLenRange)
        newCv.loc[:,'fold'] = i
        cvSet =  cvSet.append(newCv)
    cvSet.reset_index(drop=True, inplace=True)
    return cvSet


def evalPatternDistribution(data,histRange, patternLenRange, plotResults=False):
    result = pd.DataFrame()
    for histSize in histRange:
        for patternLen in patternLenRange:
            e, distribution, string, ptr, ppt = runPatternDistribution(data,
                histSize = histSize, runPeriods = 5000, patternLen = patternLen, printStats=True )
            new_result = pd.DataFrame([[histSize,patternLen,ptr,ppt,e.log]],columns = ["histSize","patternLen","ptr","ppt","log"])
            result = result.append(new_result)
    result.reset_index(drop=True, inplace=True)
    if plotResults:
        Utils.plotHeatmap(result[['histSize','patternLen','ptr']])
    return result

def runPatternDistribution(data,histSize,patternLen,runPeriods,printStats = False):
    e = pd.DataFrame()
    e, distribution, string = pattern.run(data,histSize = histSize, runPeriods = runPeriods, patternLen = patternLen )
#    ptr = e.log[e.log.pnl>0].shape[0]/e.log.shape[0]
    ptr = len([elem for elem in e.log if elem[7] > 0])/len(e.log) #count profitable trades and divide by total num of trades
    #ppt = (e.log.pnl/e.log.openPrice).sum() /e.log.shape[0]
    ppt = sum([row[7]/row[2] for row in e.log]) / len(e.log)
    if printStats:   
        print("History: " + str(histSize) +
          " Pattern length: " + str(patternLen)+ 
          " Profitable trade ratio " + "{0:.4f}".format(ptr)+
          " Avg. % profit per trade " + "{0:.6f}".format(ppt))
    return e, distribution, string, ptr, ppt


#datafile  = "USDTRY-1440-HLOC-lag0-2017.08.08.csv"
#data = Utils.readMT4data(datafile, 1000)

#datafile  = "C:\\Users\\max\\Google Drive\\Thesis\\Data\\Investing.csv"
#data = Utils.readInvData(datafile)

datafile  = r"C:\Investing.csv"
data = Utils.readInvData(datafile,200)

#datafile = "C:\\Users\\max\\Google Drive\\Thesis\\Data\\BTC_HOURLY_OHLC.csv"
#data = Utils.readBTCdata(datafile)

histRange = (10,20,30,40)
patternLenRange = (3, 4, 5, 6,7,8)
cvFold = 1
cvSet= crossValidatePatternDistribution(data,histRange, patternLenRange,cvFold)
modelPerf= evaluatePerfomance(cvSet,histRange,patternLenRange)
Utils.plotPerfHeatmap(modelPerf)
#e, distribution, string, ptr, ppt = runPatternDistribution(data,histSize=500,patternLen=6,runPeriods=5000,printStats=True)


#setptr = 0
#for index, row in cvSet.iterrows():
#    queryStr = "histSize == "+ str(10) +" and patternLen == "+ str(3)
#    print(row.results.query(queryStr))
#    if row.results.query(queryStr).ptr.values[0] >= 0.50:
#        setptr = setptr+1