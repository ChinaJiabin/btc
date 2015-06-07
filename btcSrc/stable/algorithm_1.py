#-# -*- coding: utf-8 -*-
import os
from simulateBrowser import *

'''
                     算法描述
1.事件驱动：
          事件 买：
                 当前价格低于基准价则买入，买入数量是当前价格的函数
          事件 卖：
                 (a).当前价格高于基准价_多少，则将买入的全部卖出
                 (b).当前价格高于平均买价_多少，则将买入的全部卖出
                 (c).当前价格高于部分买入的平均买价_多少，则将部分买入的全部卖出
''' 
def alg(okCoinTrade,typeTc,par):
  
  numIter  = 1
  timeSim  = datetime.datetime.now()
  
  while 1:
    #--------------------------------------------
    #确定基准价
    okCoinTrade.update(typeTc)
    basePrice  = okCoinTrade.latestPrice[typeTc] 
    print "-------------------------基准价：%s-------------------------" % basePrice
    
    buyPrice       = []
    buyAmount      = []
    buyAvgPrice    = float('inf')
    isBuy          = True
    timeStartWait  = datetime.datetime.now()
    #--------------------------------------------
    
    while 1:
       #--------------------------------
       #重新启动浏览器
       if not numIter%par['numReLogin']:
           numIter+=1
           okCoinTrade.reLogin()
       #--------------------------------

       okCoinTrade.update(typeTc)
       lastPrice = okCoinTrade.latestPrice[typeTc]

       if (not buyAmount) and \
          (datetime.datetime.now()-timeStartWait).seconds >= par['waitTime']:
          print "长时间没有买入，更换基准价!"
          break
       #---------------------------------------------------------------------------
       #事件 买 
       if ( ( not len(buyPrice) ) or lastPrice<min(buyPrice) ) \
          and lastPrice<basePrice and isBuy:
          #-----------------------------------------------
          #        查看是否由足够余额
          remainCNY = okCoinTrade.getAccount('CNY')
          buyAmount_= par['baseAmount']+par['deltaAmount']*( round(basePrice-lastPrice,2)*100 ) 
 
          if remainCNY <= lastPrice*buyAmount_:
             print "余额不足，无法购买！"
             okCoinTrade.browser.reload()
             isBuy = False
          #-----------------------------------------------
          else:
            okCoinTrade.queueAdd(typeTc+'Buy',str(lastPrice),str(buyAmount_))

            buyPrice.append(lastPrice)
            buyAmount.append(buyAmount_)
            buyAvgPrice = round( 1.0*sum(list(map(lambda x:x[0]*x[1],zip(buyPrice, buyAmount))))/sum(buyAmount),2 )

            print "买入"+typeTc+"：%s\t\t价格：%s\t\t买入均价：%s\t\t买入总数%s" \
            %( buyAmount_,lastPrice,buyAvgPrice,sum(buyAmount) )

            isBuy = False
            numIter+=1      
       #---------------------------------------------------------------------------
       #事件 卖
       elif buyPrice and \
            ( lastPrice>(buyAvgPrice+par['deltaAPrice']) or lastPrice>(basePrice+par['deltaBPrice']) ):

          okCoinTrade.queueAdd( typeTc+'Sell',str(lastPrice-0.01),str( sum(buyAmount) ) )
          print "卖出"+typeTc+"：%s\t\t价格：%s" % ( sum(buyAmount),lastPrice-0.01 )

          numIter+=1
          break
       #---------------------------------------------------------------------------
       if (datetime.datetime.now()-timeSim).seconds >= par['deltaTime']:
          print "当前时间：%s\t\t当前价格：%s" % \
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),lastPrice)
          timeSim = datetime.datetime.now()
          isBuy   = True
       time.sleep(par['updateTime'])
