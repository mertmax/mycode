# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 16:42:39 2017

@author: Efe
"""
import Utils
import matplotlib.pyplot as plt
from fbprophet import Prophet

raw_df = Utils.readMT4data("USDTRY-1440-HLOC-lag0.csv")

c = 1 #1 is High price
period = 12 # numer of periods to estimate


training_df = raw_df.ix[:raw_df.shape[0]-1-period] #leave out last rows for testing


df = training_df.ix[:, [0, c]]
df.columns = ['ds', 'y']

m = Prophet()
m.yearly_seasonality=True
m.fit(df);
future = m.make_future_dataframe(periods=period,freq='D',include_history=False)

forecast = m.predict(future)
print("\nforecast:\n" , forecast.ix[:,[0,16]])
print("\nreal:\n" , raw_df.ix[raw_df.shape[0]-period:])
#    plt.figure();
#    plt.plot(forecast.ds[:2],forecast.yhat[:2])
#    m.plot(forecast);
#    m.plot_components(forecast)

