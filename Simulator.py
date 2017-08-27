# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:28:10 2017

@author: Efe
"""
import Utils 
import PatternDistribution as pattern

import pandas as pd

def chooseModel(cvSet,histRange,patternLenRange):
    perfomances = dict();
    for histSize in histRange:
        for patternLen in patternLenRange:
            perf = 0
            for index, row in cvSet.iterrows():
                queryStr = "histSize == "+ str(histSize) +" and patternLen == "+ str(patternLen)
                perfEffect = 0
                if  row.results.query(queryStr).ptr.values[0] - 0.50 < 0:
                    perfEffect = -2*(row.results.query(queryStr).ptr.values[0] - 0.50)**2
                else:
                    perfEffect = row.results.query(queryStr).ptr.values[0] - 0.50
                perf = perf + perfEffect
                
            perfomances[(histSize,patternLen)] = perf
    return perfomances

def crossValidatePatternDistribution(allData,histRange, patternLenRange):
    cvFold = 10
    cvSet = pd.DataFrame(columns = ["data","results"])
    dataSize = int((allData.shape[0] - allData.shape[0]%cvFold)/cvFold)
    for i in range(0,cvFold,1):
        data = allData[i*dataSize:(i+1)*dataSize]
        results = evalPatternDistribution(data,histRange, patternLenRange)
        newCv = pd.DataFrame([[data,results]],columns = ["data","results"])
        cvSet =  cvSet.append(newCv)
    cvSet.reset_index(drop=True, inplace=True)
    return cvSet


def evalPatternDistribution(data,histRange, patternLenRange, plotResults=False):
    results = pd.DataFrame()
    for histSize in histRange:
        for patternLen in patternLenRange:
            e, distribution, string, ptr, ppt = runPatternDistribution(data,
                histSize = histSize, runPeriods = 20, patternLen = patternLen, printStats=True )
            new_result = pd.DataFrame([[histSize,patternLen,ptr,ppt,e]],columns = ["histSize","patternLen","ptr","ppt","e"])
            results = results.append(new_result)
    results.reset_index(drop=True, inplace=True)
    if plotResults:
        Utils.plotHeatmap(results[['histSize','patternLen','ptr']])
    return results

def runPatternDistribution(data,histSize,patternLen,runPeriods,printStats = False):
    e, distribution, string = pattern.run(data,histSize = histSize, runPeriods = runPeriods, patternLen = patternLen )
    ptr = e.log[e.log.pnl>0].shape[0]/e.log.shape[0]
    ppt = e.log.pnl.sum() /e.log.shape[0]
    if printStats:   
        print("History: " + str(histSize) +
          " Pattern length: " + str(patternLen)+ 
          " Profitable trade ratio " + "{0:.2f}".format(ptr)+
          " Avg. profit per trade " + "{0:.4f}".format(ppt))
    return e, distribution, string, ptr, ppt


#datafile  = "USDTRY-1440-HLOC-lag0-2017.08.08.csv"
#data = Utils.readMT4data(datafile, 1000)

datafile  = "C:\\Users\\max\\Google Drive\\Thesis\\Data\\Investing.csv"
data = Utils.readInvData(datafile)
histRange = (10, 20, 40, 80, 160, 250) #range(8,308,100)
patternLenRange = range(2,6,1)
cvSet= crossValidatePatternDistribution(data,histRange, patternLenRange)
modelPerf= chooseModel(cvSet,histRange,patternLenRange)

