# -*- coding: utf-8 -*-
#邮箱
email       = "489509928@qq.com"
#密码 
password    = "lan@2014" 

      #交易虚拟币类型（比特币或莱特币）
par={ 'typeTc'           :'ltc',     
      #浏览器重新登录间隔，值越大间隔越久，为防止卡死
      'numReLogin'       :20,
      #单笔交易虚拟币数量
      'amount'           :0.1, 
      #卖出队列前__多少条的均价   
      'statSellNum'      :5,
      #卖出队列前__多少条的均价     
      'statBuyNum'       :1,
      #向终端打印信息的时间间隔      
      'waitTime'         :10,
      #两次自动交易的时间间隔
      'deltaTime'        :3   } 
  
#------------------------
# 在此选择所需要的算法
from algorithm_3 import *
#------------------------
   
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
