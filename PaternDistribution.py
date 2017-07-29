# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 22:23:35 2017

PaternDistribution

@author: Efe
"""
import itertools 
import Utils

#represent timeseries with categorical attributes
def convertTimeseries(df):
    string = ''
    returns = df.h.diff()
    for index, row in df.iterrows():
        if index == 0:
            continue
        if returns.ix[index] >= 0:
            string = string + "u"
        else:
            string = string + "d"
            
        if df.v[index] > 60000:
            string = string + "V"
        else:
            string = string + "v"
    return string

#generate patterns of categorical attributes and calculate probabilities for each
def generateDistribution(string):
    terms = []
    tmp = ''
    for i in itertools.product(itertools.product('ud','Vv'), repeat = 2):
        for ii in i:
            tmp= tmp + ii[0]+ii[1]
        terms.append(tmp)
        tmp = ''  
    distribution = dict()
    for t in terms:
        distribution[t] = string.count(t)
    total = sum(distribution.values())
    for key, value in distribution.items():
        distribution[key] = value / total
    return distribution

#re-calculate probabilities given part of the pattern has been observed
def distributionGivenFirstTerm(firstTerm, distribution):
    newDict = dict()
    ftLen = len(firstTerm)
    for key, value in distribution.items():
        if key.startswith(firstTerm):
            newDict[key[ftLen:]] = value
    total = sum(newDict.values())
    for key, value in newDict.items():
        newDict[key] = value / total  
    return newDict

df = Utils.readMT4data("USDTRY-1440-HLOC-lag0.csv")
string = convertTimeseries(df)
distribution = generateDistribution(string)
newDict = distributionGivenFirstTerm('uV',distribution)