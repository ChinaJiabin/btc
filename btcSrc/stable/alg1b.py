#-# -*- coding: utf-8 -*-
import datetime
from okCoin import *

def alg(okCoinTrade,par):
  
    timeSim  = datetime.datetime.now()
    while 1:
      #--------------------------------------------
      #确定基准价
      basePrice  = float( okCoinTrade.getTicker()['ticker']['last'] )
      print "-------------------------基准价：%s-------------------------"\
      % basePrice
      
      buyPrice       = []
      buyAmount      = []
      buyAvgPrice    = float('inf')
      isBuy          = True
      timeStartWait  = datetime.datetime.now()
      #--------------------------------------------
      
      while 1:
	lastPrice = float( okCoinTrade.getTicker()['ticker']['last'] )

	if (not buyAmount) and \
	    (datetime.datetime.now()-timeStartWait).seconds >= par['waitTime']:
	    print "长时间没有买入，更换基准价!"
	    break
	#---------------------------------------------------------------------------
	#事件 买 
	if ( ( not len(buyPrice) ) or lastPrice<min(buyPrice) ) \
	    and lastPrice<basePrice and isBuy:
	  
	    buyAmount_= par['baseAmount']+par['deltaAmount']*( round(basePrice-lastPrice,2)*100 ) 
  
	    try:
	      okCoinTrade.trade( 'buy',lastPrice,buyAmount_ )

	      buyPrice.append(lastPrice)
	      buyAmount.append(buyAmount_)
	      buyAvgPrice = round( 1.0*sum(list(map(lambda x:x[0]*x[1],zip(buyPrice, buyAmount))))/sum(buyAmount),2 )

	      print "买入"+okCoinTrade.typeTc+"：%s\t\t价格：%s\t\t买入均价：%s\t\t买入总数%s" \
	      %( buyAmount_,lastPrice,buyAvgPrice,sum(buyAmount) )
	      isBuy = False  

	    except Exception as e:
	      if e.message == "error code 10010": 
		print "余额不足，无法交易"  
	      else:
		print e
		return
	#---------------------------------------------------------------------------
	#事件 卖
	elif buyPrice and \
	      ( lastPrice>(buyAvgPrice+par['deltaAPrice']) or lastPrice>(basePrice+par['deltaBPrice']) ):
	    
	    try:
	      sellOrderId = okCoinTrade.trade( 'sell', lastPrice-0.01, sum(buyAmount) )

	      print "卖出"+okCoinTrade.typeTc+"：%s\t\t价格：%s" % ( sum(buyAmount),lastPrice-0.01 )
	      #---------------------------------------  
	      #等待卖 事件 完成
	      numIter = 0
	      while not okCoinTrade.isDeal(sellOrderId):
		print "等待卖交易完成\t\t%s"\
		%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		time.sleep(20)

		numIter +=1
		if numIter == 6:
		  break
	      #---------------------------------------
	      break
  
	    except Exception as e:
	      if e.message == "error code 10010": 
		print "余币不足，无法全部卖出"  
	      else:
		print e
		return
	#---------------------------------------------------------------------------
	if (datetime.datetime.now()-timeSim).seconds >= par['deltaTime']:
	    print "当前时间：%s\t\t当前价格：%s" % \
	    (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),lastPrice)
	    timeSim = datetime.datetime.now()
	    isBuy   = True
	time.sleep(par['updateTime'])  
