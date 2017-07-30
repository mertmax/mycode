# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 22:23:35 2017

PaternDistribution

@author: Efe
"""
import itertools 
import Utils
import Engine as en

termLen = 2
patternLen = 2 

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
    for i in itertools.product(itertools.product('ud','Vv'), repeat = patternLen):
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

def suggestTrade(string,distribution):
    newDist =  distributionGivenFirstTerm(
            string[-termLen*(patternLen-1):], distribution) #feed the last realized terms as fisrst terms to get suggestion
    print(string[-termLen*(patternLen-1):])
    print(newDist)
    buy = 0
    sell = 0
    for key, value in newDist.items():
        if key.startswith('u'):
            buy = buy + value
        if key.startswith('d'):
            sell = sell + value
    total = sum(newDist.values())
    buy = buy / total
    sell = sell / total
    if (buy>=sell):
        print("Price increase with probability:",buy)
        return 1 
    else:
        print("Price decrease with probability:",sell)
        return -1
    return 'error'
    
#df = Utils.readMT4data("USDTRY-1440-HLOC-lag0.csv")
#string = convertTimeseries(df)
#distribution = generateDistribution(string)
#sug = suggestTrade(string,distribution)

raw_df = Utils.readMT4data("USDTRY-1440-HLOC-lag0.csv")

init_string = convertTimeseries(raw_df)
init_distribution = generateDistribution(init_string)


e = en.Engine(raw_df[['time','h','v']],364)

while e.hasNext == True:
    string = convertTimeseries(e.hist)
    distribution = generateDistribution(string)
    sug = suggestTrade(string,distribution)
    
    e.openPos()
    e.next()
    e.closePos()

print(e.log)
    