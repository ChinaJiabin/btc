# -*- coding: utf-8 -*-
import os
from simulateBrowser import *

'''
                      算法描述
1.时间驱动：每隔一段时间向买和卖队列同时插入一个事件
2.价格设定：买价低于卖价且大于等于当前价，卖价为卖队列中前数条的均价
'''

def alg(okCoinTrade,typeTc,par):
  
  numIter = 0
  while 1:
  #----------------------------------------------------------------------------
  #1.
    TimeSim = datetime.datetime.now()
    numIter+= 1
    if not numIter%par['numReLogin']:
       okCoinTrade.reLogin()
       
    while 1:
      buyPrice  = okCoinTrade.averagePrice(par['statBuyNum'],'Buy',typeTc)
      sellPrice = okCoinTrade.averagePrice(par['statSellNum'],'Sell',typeTc)
      
      print "买入价：%s\t\t卖出价：%s" %(buyPrice,sellPrice)
      
      if buyPrice<sellPrice:
        
         try:
	   okCoinTrade.queueAdd(typeTc+'Buy',str(buyPrice),str(par['amount']))
	   okCoinTrade.queueAdd(typeTc+'Sell',str(sellPrice),str(par['amount']))
	   break
         except:
           print "--------------------New start--------------------"
           okCoinTrade.reLogin()

  #----------------------------------------------------------------------------
  #2.
    while 1:
      #-----------------------------------------
      #等待停止：2. 等待时间过长
      time.sleep(par['waitTime'])
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )
      
      if datetime.datetime.now()>(TimeSim+datetime.timedelta(minutes=par['deltaTime'])):
	break     

