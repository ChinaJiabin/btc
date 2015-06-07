# -*- coding: utf-8 -*-
import os
from okCoin import *

'''
                      算法描述
1.时间驱动：每隔一段时间向买和卖队列同时插入一个事件
2.价格设定：买价低于卖价且大于等于当前价，卖价为卖队列中前数条的均价
'''

def alg(okCoinTrade,par):
  
  while 1:
  
    TimeSim = datetime.datetime.now()

    while 1:

      buyPrice,sellPrice  = okCoinTrade.averagePrice(par['statBuyNum'],par['statSellNum'])
     
      if buyPrice<sellPrice:

         okCoinTrade.trade( 'buy',buyPrice,par['amount'] )
         okCoinTrade.trade( 'sell',sellPrice,par['amount'] )

         print "买入价：%s\t\t卖出价：%s" %(buyPrice,sellPrice)

         break

    while 1:

      time.sleep(par['waitTime'])
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )
      
      if datetime.datetime.now()>(TimeSim+datetime.timedelta(minutes=par['deltaTime'])):
	break     

