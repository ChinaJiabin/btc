# -*- coding: utf-8 -*-
#邮箱
email       = "489509928@qq.com"
#密码 
password    = "lan@2014" 


      #交易虚拟币类型（比特币或莱特币）
par={ 'typeTc'           :'ltc',  
      #浏览器重新登录间隔，值越大间隔越久，为防止卡死
      'numReLogin'       :20,

      #先买再卖的单笔交易数量
      'upAmount'         :1, 
      #先卖再买的单笔交易数量
      'downAmount'       :2,

      #先买再卖 前__多少条的均价   
      'upSellNum'        :8,
      #先卖再买 前__多少条的均价     
      'downBuyNum'       :8,
    
      #获取当前价的时间间隔（单位秒）      
      'updateTime'       :3,   
      #两个事件发生的最短时间间隔 （单位秒）
      'deltaTime'        :2*60, 
      #打印时间信息的时间间隔 （单位秒）
      'printTime'        :5*60 } 
  
#------------------------
# 在此选择所需要的算法
from algorithm_2 import *
#------------------------


okCoinTrade = autoTrade(email,password)
alg(okCoinTrade,par['typeTc'],par)

'''
while 1:

  try:
      
      while 1:
	try:
	  okCoinTrade = autoTrade(email,password)
	  break
	except:
	  print "Please check net connect^_^" 
	  time.sleep(60)
	    
      alg(okCoinTrade,par['typeTc'],par)
  except:
      if okCoinTrade:
	 del okCoinTrade	
      print("-----------------------New-----------------------")
'''
