#-# -*- coding: utf-8 -*-
import os
from numpy import *
from simulateBrowser import *

'''
                     算法描述
1.事件驱动：
          事件 卖：
                 当前价格高于基准价则卖出，卖出数量是当前价格的函数
          事件 买：
                 (a).当前价格低于基准价_多少  则将卖出的全部买入
                 (b).当前价格低于平均卖价_多少 则将卖出的全部买入
                 (c).当前价格低于部分卖出的平均卖价_多少 则将部分卖出的全部买入
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
    
    sellPrice       = array([])
    sellAvgPrice    = []
    sellTotalAmount = 0
    isSell          = True
    timeStartWait   = datetime.datetime.now()
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

       if (not sellTotalAmount) and \
          (datetime.datetime.now()-timeStartWait).seconds >= par['waitTime']:
          print "长时间没有买入，更换基准价!"
          break
       #--------------------------------------------------------------------------------
       #事件 卖 
       if ( (not len(sellPrice) ) or lastPrice>max(sellPrice) ) \
          and lastPrice>basePrice and isSell:
          #-------------------------------------------
          #        查看是否由足够余币
          remainTc = okCoinTrade.getAccount(typeTc) 
          if remainTc <= par['sellAmount']:
             print "余币不足，无法卖出！"
             isSell = False
          #-------------------------------------------
          else:
            okCoinTrade.queueAdd(typeTc+'Sell',str(lastPrice-0.01),str(par['sellAmount']))

            sellPrice    = hstack([sellPrice,(lastPrice-0.01)])
            sellAvgPrice = round(sum(sellPrice)/len(sellPrice),2)
            sellTotalAmount+=par['sellAmount']

            print "卖出"+typeTc+"：%s\t\t价格：%s\t\t卖出均价：%s\t\t卖出总数%s" \
            %(par['sellAmount'],lastPrice-0.01,sellAvgPrice,sellTotalAmount)

            isSell = False
            numIter+=1      
       #--------------------------------------------------------------------------------
       #事件 买
       elif len(sellPrice) and \
            ( lastPrice<(sellAvgPrice-par['deltaAPrice']) or lastPrice<(basePrice-par['deltaBPrice']) ):

          okCoinTrade.queueAdd(typeTc+'Buy',str(lastPrice+0.01),str(sellTotalAmount))
          print "买入"+typeTc+"：%s\t\t价格：%s" % (sellTotalAmount,lastPrice+0.01)

          numIter+=1
          break
       
       elif len(sellPrice) >= par['minPartBuy']:
            sellPartAvgPrice = ( cumsum(sellPrice[::-1])/cumsum( ones( len(sellPrice) ) ) )[::-1]
            partId=( ( sellPartAvgPrice-(lastPrice+par['deltaAPrice']) )>0 ).nonzero()
            if partId.any():
               partId = partId[0][0]
               sellPartAmount = par['sellAmount']*(len(sellPrice)-partId)
               okCoinTrade.queueAdd(typeTc+'Buy',str(lastPrice+0.01),str(sellPartAmount))
               print "部分买入"+typeTc+"：%s\t\t价格：%s" % (sellPartAmount,lastPrice+0.01)

               sellPrice       = sellPrice[0:partId]
               sellTotalAmount-= sellPartAmount

               numIter+=1
               continue
       #--------------------------------------------------------------------------------
       if (datetime.datetime.now()-timeSim).seconds >= par['deltaTime']:
          print "当前时间：%s\t\t当前价格：%s" % \
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),lastPrice)
          timeSim = datetime.datetime.now()
          isSell  = True
       time.sleep(par['updateTime'])
