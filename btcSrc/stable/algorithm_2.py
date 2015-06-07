#-# -*- coding: utf-8 -*-
import os
from simulateBrowser import *

'''
                     算法描述
1.事件驱动：
                     事件1
        ---------------------------------
         事件描述： 当前价买入，更高价卖出

         触发条件： 当前价高于上限价
        ---------------------------------
   
                     事件2
        ---------------------------------
         事件描述： 当前价卖出，更底价卖入       
                                        
         触发条件： 当前价底于上限价
        ---------------------------------

                     事件3
        ---------------------------------
         事件描述： 事件1结束

         触发条件： 当前价高于最高挂单价
        ---------------------------------
            
                     事件4
        ---------------------------------
         事件描述： 事件2结束

         触发条件： 当前价低于最低挂单价
        ---------------------------------   
''' 
def alg(okCoinTrade,typeTc,par):

    #--------------------------------------------------
    #确定初始上限价和下限价
    okCoinTrade.update(typeTc)
    upPrice   = okCoinTrade.latestPrice[typeTc] + 0.01
    downPrice = okCoinTrade.latestPrice[typeTc] - 0.01
    
    print "上限价：%s\t\t下限价：%s" % \
          (upPrice,downPrice)
    
    isOverEvent_1 = True
    isOverEvent_2 = True

    maxPrice = float("inf")
    minPrice = float("-inf")
    #--------------------------------------------------
    timeSim = datetime.datetime.now()
    numIter = 1
    while 1:
        
        if not numIter%par['numReLogin']:
           numIter+=1
           okCoinTrade.reLogin()

	okCoinTrade.update(typeTc)
        lastPrice = okCoinTrade.latestPrice[typeTc]
        #------------------------------------------------------------------------------------
        #事件1
	if lastPrice > upPrice and isOverEvent_1: 
	  
	   buyPrice  = lastPrice
	   sellPrice = okCoinTrade.averagePrice(par['upSellNum'],'Sell',typeTc)
	    
	   if buyPrice<sellPrice:
	      okCoinTrade.queueAdd(typeTc+'Buy',str(buyPrice),str(par['upAmount']))
              okCoinTrade.queueAdd(typeTc+'Sell',str(sellPrice),str(par['upAmount']))
              print "先买后卖事件\t\t买入价：%s\t\t卖出价：%s" %(buyPrice,sellPrice)
              #---------------------
              maxPrice = sellPrice
              isOverEvent_1 = False
              numIter+=1
              #---------------------         	  
	#------------------------------------------------------------------------------------ 
        #事件2   
	elif lastPrice < downPrice and isOverEvent_2: 
	     
	     buyPrice  = okCoinTrade.averagePrice(par['downBuyNum'],'Buy',typeTc)
	     sellPrice = lastPrice
		
	     if buyPrice<sellPrice:
	        okCoinTrade.queueAdd(typeTc+'Buy',str(buyPrice),str(par['downAmount']))
	        okCoinTrade.queueAdd(typeTc+'Sell',str(sellPrice),str(par['downAmount']))
                print "先卖后买事件\t\t买入价：%s\t\t卖出价：%s" %(buyPrice,sellPrice)
                #---------------------
                minPrice = buyPrice
                isOverEvent_2 = False
                numIter+=1
                #---------------------
        #------------------------------------------------------------------------------------
        #事件3
        elif lastPrice > maxPrice:
             isOverEvent_1 = True
             time.sleep(par['deltaTime'])
        #------------------------------------------------------------------------------------
        #事件4
        elif lastPrice < minPrice:
             isOverEvent_2 = True 
             time.sleep(par['deltaTime'])
        #------------------------------------------------------------------------------------
        if (datetime.datetime.now()-timeSim).seconds >= par['printTime']:
           timeSim = datetime.datetime.now()
           print "当前时间：%s\t\t当前价：%s" % \
                 (timeSim.strftime("%Y-%m-%d %H:%M:%S"),lastPrice)
	time.sleep(par['updateTime'])
