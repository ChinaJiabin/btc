# -*- coding: utf-8 -*-
import datetime
from okCoin import *

def alg(okCoinTrade,par):
  
  timeSim  = datetime.datetime.now()
  while 1:
    #--------------------------------------------
    #确定基准价
    basePrice  = float( okCoinTrade.getTicker()['ticker']['last'] )
    print "-------------------------基准价：%s-------------------------" \
          % basePrice
    
    sellPrice       = []
    sellAmount      = []
    sellAvgPrice    = float('-inf')
    isSell          = True
    timeStartWait   = datetime.datetime.now()
    #--------------------------------------------
    
    while 1:
       lastPrice = float( okCoinTrade.getTicker()['ticker']['last'] )

       if (not sellAmount) and \
          (datetime.datetime.now()-timeStartWait).seconds >= par['waitTime']:
          print "长时间没有买入，更换基准价!"
          break
       #--------------------------------------------------------------------------------
       #事件 卖 
       if ( (not len(sellPrice) ) or lastPrice>max(sellPrice) ) \
          and lastPrice>basePrice and isSell:
         
          sellAmount_= par['baseAmount']+par['deltaAmount']*( round( (lastPrice-basePrice),2)*100 ) 
          
          try:
            okCoinTrade.trade( 'sell',lastPrice,sellAmount_ )
  
            sellPrice.append(lastPrice)
            sellAmount.append(sellAmount_)
            sellAvgPrice =round( 1.0*sum(list(map(lambda x:x[0]*x[1],zip(sellPrice, sellAmount))))/sum(sellAmount),2 )

            print "卖出"+okCoinTrade.typeTc+"：%s\t\t价格：%s\t\t卖出均价：%s\t\t卖出总数%s" \
            %( sellAmount_,lastPrice,sellAvgPrice,sum(sellAmount) )           
            isSell = False  

          except Exception as e:
            if e.message == "error code 10010": 
               print "余币不足，无法交易"  
            else:
               print e
               return
       #--------------------------------------------------------------------------------
       #事件 买
       elif len(sellPrice) and \
            ( lastPrice<(sellAvgPrice-par['deltaAPrice']) or lastPrice<(basePrice-par['deltaBPrice']) ):

          try:
            buyOrderId = okCoinTrade.trade( 'buy', lastPrice+0.01, sum(sellAmount) )

            print "买入"+okCoinTrade.typeTc+"：%s\t\t价格：%s" % ( sum(sellAmount),lastPrice+0.01 )
            #---------------------------------------  
            #等待买 事件 完成
            numIter = 0
            while not okCoinTrade.isDeal(buyOrderId):
              print "等待买交易完成\t\t%s"\
              %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
              time.sleep(20)
              
              numIter+=1
              if numIter == 6:
                 break
            #---------------------------------------
            break

          except Exception as e:
            if e.message == "error code 10010": 
               print "余额不足，无法全部买入"  
            else:
               print e
               return
       #--------------------------------------------------------------------------------
      
       if (datetime.datetime.now()-timeSim).seconds >= par['deltaTime']:
          print "当前时间：%s\t\t当前价格：%s" % \
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),lastPrice)
          timeSim = datetime.datetime.now()
          isSell  = True
       time.sleep(par['updateTime'])
