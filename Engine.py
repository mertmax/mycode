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
import datetime

class Engine(object):
    log = pd.DataFrame(columns = ['openTime', 'side','openPrice', 'SL', 'TP',
                                  'closeTime', 'closePrice', 'pnl', 'comment'])
   
   #potentially add max drawdown to log
   
    def __init__(self,args,histLen):
        self.hist = args[:histLen]
        self.priceData = args[histLen:].reset_index(drop=True)
        self.t = 0
        self.hasNext = True
        
        
    def openPos(self,side,comment = ""):
        #side: 1 for buy, -1 for sell
        newTrade = pd.DataFrame([[self.priceData.ix[self.t].time, side, self.priceData.ix[self.t].tPrice ,0.0,0.0,datetime.datetime(9999,12,31),0.0,0.0,comment]],[self.log.shape[0]], columns = ['openTime', 'side',
        'openPrice', 'SL', 'TP', 'closeTime', 'closePrice', 'pnl', 'comment']) #open at tPrice of the period
        self.log = self.log.append(newTrade)
        
    def closePos(self):
        last = self.log.shape[0]-1
        closeprice= self.priceData.tPrice[self.t]
        self.log.set_value(last,'closePrice',closeprice)
        self.log.set_value(last,'closeTime',self.priceData.time[self.t])
        self.log.set_value(last,'pnl',self.log['side'][last]*(
                closeprice - self.log['openPrice'][last]))
        
    def next(self):
        
        if(self.t+1 < self.priceData.shape[0]):          
            self.hist = self.hist[1:]
            self.hist = self.hist.append(self.priceData.ix[self.t], ignore_index=True)
            self.t = self.t+1
        else:
            self.hasNext = False
            
    def reportLog(self):
        ptr = self.log[self.log.pnl>0].shape[0]/self.log.shape[0]
        ppt = self.log.pnl.sum() /self.log.shape[0]
        print("Profitable trade ratio " + str(ptr)+
              " Avg. profit per trade " + str(ppt))