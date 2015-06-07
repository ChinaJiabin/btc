# -*- coding: utf-8 -*-
import os
import random
import scipy.stats
from numpy import *
from okCoin import *

'''
                    算法描述
1.时间驱动：每隔一段时间向买或卖队列插入一个事件
2.正态分布：假设一段时间的成交价呈正态分布
3.判断涨跌：通过正态分布的累计概率密度函数计算当前成交价的涨跌概率
4.贪心算法：如果预测涨则买，跌则卖
'''

def normPredict(lastPrice):
  
  expect  = sum(LastPrice)/len(LastPrice)
  var     = sum([(x-expect)**2 for x in LastPrice])/(len(LastPrice)-1)
  nowNorm = scipy.stats.norm(expect,var**0.5)
  proFall = nowNorm.cdf(LastPrice[-1])
  
  print "期望：%s\t方差：%s\t当前价：%s\t下跌概率：%s" \
        %(expect,var,LastPrice[-1],proFall)
  return random.random()<proFall
 
 
def alg( okCoinTrade, par ):
 
    lastPrice = [] 
    while len(LastPrice)<par['minNum']:
      time.sleep(par['recordTime'])
      lastPrice.append( okCoinTrade.getTicker['ticker']['last'] )
      print "初始记录数据中，请等待！"
   
    TimeSim = datetime.datetime.now()
    predictTime = TimeSim+datetime.timedelta(minutes=par['deltaTime'])
    
    if normPredict(lastPrice):
       sellPrice = LastPrice[-1]-0.05 
       okCoinTrade.trade( 'sell', sellPrice, par['amount'] )
       print "事件：卖\t\t价格：%s" % sellPrice
    else: 
       buyPrice  = LastPrice[-1]+0.05
       okCoinTrade.trade( 'buy', buyPrice, par['amount'] )
       print "事件：买\t\t价格：%s" % buyPrice
    
    while 1:
      lastPrice.append( okCoinTrade.getTicker['ticker']['last'] )
      time.sleep(par['recordTime'])
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )
      if datetime.datetime.now()>predictTime
         break
