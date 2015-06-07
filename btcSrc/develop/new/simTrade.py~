# -*- coding: utf-8 -*-
import urllib2
import json
import time

class historyData:

  def __init__(self,typeTc):
      self.typeTc = typeTc

  def getRecord(self,orderId):
      html = urllib2.urlopen( \
      'https://www.okcoin.cn/api/trades.do?symbol='+self.typeTc+'_cny&since=%s' % orderId \
                            ).read()
      return json.loads(html)

class simAccount:
  
  def __init__( self, balanceCny,balanceTc ):
    self.balanceCny = balanceCny
    self.balanceTc  = balanceTc

  def buy(self,price,amount):
    if self.balanceCny >= price*amount:
       self.balanceCny -= price*amount
       self.balanceTc  += amount
       return True
    return False 

  def sell(self,price,amount):
    if self.balanceTc  >= amount:
       self.balanceCny += price*amount
       self.balanceTc  -= amount
       return True
    return False
 
class simTrade( historyData, simAccount ):

  def __init__( self, typeTc, startTime, endTime, balanceCny, balanceTc ):
    historyData.__init__(self, typeTc )
    simAccount.__init__( self, balanceCny,balanceTc )
   
    self.startTime = int( time.mktime( time.strptime(startTime, "%Y-%m-%d %H:%M:%S") ) )
    self.endTime   = int( time.mktime( time.strptime(endTime, "%Y-%m-%d %H:%M:%S") ) )

    self.buyPrice  = []
    self.sellPrice = []
    
    self.isBuy   = False
    self.isSell  = False

    self.isStart = False
    self.isEnd   = False

  def simTrade(self):

      startId = 0
      while 1:
        record = self.getRecord(startId)
        for i in range( len(record) ):
            self.alg(record[i])

        if self.isStart and not self.isEnd:      
           self.printInfo(record[-1])
           startId = record[-1]['tid']
        elif self.isEnd:
           return 
   
  def alg( self, data ):

    if self.startTime <= data['date'] and self.endTime >= data['date']:
       if not self.isStart:
          self.isStart = True

       lastPrice = float(data['price'])
       if not self.isSell:
          if self.buy(lastPrice,1):
             self.buyPrice = lastPrice
             self.isSell = True
       elif lastPrice > self.buyPrice+0.5:
           if self.sell(lastPrice,1):
              self.isSell = False
        

    elif self.endTime < data['date']:
         self.isEnd = True 

  def printInfo( self, data ):
    
    print "人名币总数：%s\t\t虚拟币总数：%s\t\t时间：%s" \
    %( self.balanceCny,self.balanceTc,time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(data['date']) ) ) 
    
if __name__=="__main__":  
   okSimTrade = simTrade( 'ltc', '2013-9-23 00:00:00', '2014-12-31 00:00:00', 5000, 0 )
   okSimTrade.simTrade()

