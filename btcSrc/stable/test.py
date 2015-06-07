# -*- coding: utf-8 -*-
from okCoin import *

okCoinTrade = okCoin('ltc', 0, 0)

a,b = okCoinTrade.averagePrice(5,5)

print a,b
'''
#多线程示例
class threadGetLastPrice(threading.Thread,obtainData):
  def __init__(self,typeTc,updateTime):
      threading.Thread.__init__(self)
      obtainData.__init__(self)
      self.typeTc      = typeTc
      self.updateTime  = updateTime
      self.keepRunning = True
      self.lastPrice   = []

  def run(self):
      while self.keepRunning:
        self.update(self.typeTc)
        self.lastPrice = (datetime.datetime.now(),self.latestPrice[self.typeTc]) 
        time.sleep(self.updateTime)

  def stop(self):
      self.keepRunning = False
'''
