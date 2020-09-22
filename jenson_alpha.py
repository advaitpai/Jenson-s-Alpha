#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 00:09:48 2020

@author: advait
"""

import pandas as pd
import numpy as np
import statistics
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


file_name = 'Test.xlsx'
sheet_names = ['Axis','HDFC','UTI','Tata','ICICI','LIC','Franklin','Sundaram','SBI','Nifty']

avg_hpr1 = []
ann_hpr1 = []
stdv_hpr1 = []
ann_stdv1 = []
hpr_list = []

for s in sheet_names:
    print ("\nSheet Name:- ",s)
    datapoints = pd.read_excel(file_name,s)
    #print (datapoints)
    
    adj_close = datapoints['Adj Close']
    hpr = [0]

    for i in range(1,len(adj_close)):
        x = (adj_close[i]-adj_close[i-1])/adj_close[i-1]*100
        hpr.append(x)

    datapoints['HPR'] = hpr
    #print (datapoints)

    avg_hpr = statistics.mean(hpr[1:]) #[1:] indicates we're extracting from second position
    ann_hpr = avg_hpr*12
    stdv_hpr = statistics.stdev(hpr[1:]) 
    ann_stdv = stdv_hpr*(12**(1/2))
    
    #Add to list of values
    avg_hpr1.append(avg_hpr)
    ann_hpr1.append(ann_hpr)
    stdv_hpr1.append(stdv_hpr)
    ann_stdv1.append(ann_stdv)
    hpr_list.append(hpr)

    print ("Average HPR: ", avg_hpr)
    print ("Annualised Average HPR: ", ann_hpr)
    print ("Standard Deviation of HPR: ", stdv_hpr)
    print ("Annualised Deviation of HPR: ", ann_stdv)

    
plot = LinearRegression()
x = np.array(hpr_list[-1]) #HPR List of Nifty
x = x.reshape(-1,1)

risk_free = 5.37

print ("\nFINAL RESULTS:-")
for i in range(0,len(hpr_list)-1): #Starts calculating for every sheet
    print("\nCompany Name:-",sheet_names[i])
    y = np.array(hpr_list[i])  #HPR List of Respective Company
    y = y.reshape(-1,1)
    plot.fit(x,y)
    slope = plot.coef_[0][0]
    print ('Slope:-',slope)
    alpha = ann_hpr1[i]-(risk_free+(slope*(ann_hpr1[-1]-risk_free)))
    print ("Jenson's Alpha Value:-",alpha)

datapoints = pd.read_excel(file_name,'Nifty')
dates = list(datapoints['Date'])
leg = []
for i in range(0,len(sheet_names)):
    plt.plot(dates,hpr_list[i])
    leg.append(sheet_names[i])
plt.legend(leg)
plt.show()
    

