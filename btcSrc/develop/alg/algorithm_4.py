# -*- coding: utf-8 -*-
import os
import datetime
from numpy import *
from simulateBrowser import *

'''
                    算法描述
1.时间驱动：每隔一段时间向买或卖队列插入一个事件
2.回归预测：记录前一段时间的成交价预测未来一段时间的成交价
3.判断涨跌：通过回归系数判断涨跌
4.贪心算法：如果预测涨则买，跌则卖
'''

LastPrice  = []
GetData    = obtainData()

def recordLastPrice(typeTc,maxNum):
  
  GetData.update(typeTc)
  LastPrice.append([datetime.datetime.now(),GetData.latestPrice[typeTc]])
  if len(LastPrice)>maxNum:
    del LastPrice[0]
  
def regressionPredict(predictTime):
  
  N = len(LastPrice)
  xArr = array([[1,(x[0]-LastPrice[0][0]).seconds] for x in LastPrice])
  yArr = array([[x[1]] for x in LastPrice]) 
  
  q,r = linalg.qr(xArr)
  ws  = linalg.solve(r,dot(q.T,yArr))
  
  return ws[1]>0
 
def alg(okCoinTrade,typeTc,par):
  
  numIter = 0
  while 1:
   
    numIter+=1
    if not numIter%par['numReLogin']:
       okCoinTrade.reLogin()
    #----------------------------------------------------------------------------
    #1.
    while len(LastPrice)<par['minNum']:
      time.sleep(par['recordTime'])
      recordLastPrice('ltc',par['maxNum'])
      print "waiting!"
   
    TimeSim = datetime.datetime.now()
    predictTime = TimeSim+datetime.timedelta(minutes=par['deltaTime'])
    
    try:
      if regressionPredict(predictTime):
	buyPrice  = LastPrice[-1][1]+0.05
	okCoinTrade.queueAdd(typeTc+'Buy', str(buyPrice),str(par['amount']))
	print "Deal type:Buy\t\tPrice:%s " % buyPrice
      else: 
	sellPrice = LastPrice[-1][1]-0.05 
	okCoinTrade.queueAdd(typeTc+'Sell',str(sellPrice),str(par['amount']))
	print "Deal type:Sell\t\tPrice:%s" % sellPrice
    except:
      time.sleep(60)
      print "--------------New start--------------"
      okCoinTrade.reLogin()
      continue
    
    #----------------------------------------------------------------------------
    #2.
    while 1:
      recordLastPrice('ltc',par['maxNum'])
      time.sleep(par['recordTime'])
      print(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) )
      if datetime.datetime.now()>(TimeSim+datetime.timedelta(minutes=par['deltaTime'])):
	break
  #----------------------------------------------------------------------------
  
