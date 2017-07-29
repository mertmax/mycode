# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 17:51:25 2017

Engine for forex trade simulation

initialize: get price timeseries and set up trade log
openPos: post an open trade account with opening time, buy/sell
     opening price, tp, sl 
closePos: modify trade log to close a pos with closing time, closing price, pnl

next: move onto next point in time and price, execute TP and SL, update account

@author: Efe
"""
import pandas as pd
import Utils

class Engine(object):
    log = pd.DataFrame(columns = ['openTime', 'side','openPrice', 'SL', 'TP',
                                  'closeTime', 'closePrice', 'pnl'])
    
   #potentially add max drawdown to log
   
    def __init__(self,args):
        self.priceData = args
        self.t = 0
        self.hasNext = True
        
    def openPos(self):
        #side: 1 for buy, -1 for sell
        newTrade = pd.DataFrame([[self.priceData.ix[self.t].time,-1,self.priceData.ix[self.t].h,0.0,0.0,0.0,0.0,0.0]],[self.log.shape[0]], columns = ['openTime', 'side',
        'openPrice', 'SL', 'TP', 'closeTime', 'closePrice', 'pnl'])
        self.log = self.log.append(newTrade)
        
    def closePos(self):
        last = self.log.shape[0]-1
        self.log['closePrice'][last] = self.priceData.ix[self.t].h
        self.log['closeTime'][last] = self.priceData.ix[self.t].time
        self.log['pnl'][last] = self.log['side'][last]*(
                self.log['closePrice'][last] - self.log['openPrice'][last] ) 
        
    def next(self):
        
        if(self.t+1 < self.priceData.shape[0]):
            self.t = self.t+1
        else:
            self.hasNext = False 


#test code

raw_df = Utils.readMT4data("USDTRY-1440-HLOC-lag0.csv")
raw_df = raw_df[:10]

a = Engine(raw_df[['time','h']])

while a.hasNext == True:
    a.openPos()
    a.next()
    a.closePos()
    print(a.log)
    
