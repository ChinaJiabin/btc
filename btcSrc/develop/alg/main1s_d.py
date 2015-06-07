# -*- coding: utf-8 -*-
#邮箱
email       = "489509928@qq.com"
#密码 
password    = "lan@2014" 

      #浏览器重新登录间隔，值越大间隔越久，为防止卡死
par={ 'numReLogin'       :10,
      #当前价小于卖出均价_多少 则全买入（单位:元）
      'deltaAPrice'      :0.1,
      #当前价小于基准价_多少 则全买入（单位:元）
      'deltaBPrice'      :0.03,
      #单笔卖交易数量
      'sellAmount'       :0.1,    
      #获取当前价的时间间隔（单位:秒）      
      'updateTime'       :5,
      #插入第一笔卖事件的最长等待时间（单位：秒）
      'waitTime'         :3*60,
      #两笔卖交易发生的最短时间间隔（单位:秒）
      'deltaTime'        :2*60, 
      #买入部分时，最小卖出笔数
      'minPartBuy'       :5 } 
  
#------------------------
# 在此选择所需要的算法
from algorithm_1s import *
#------------------------


okCoinTrade = autoTrade(email,password)
alg(okCoinTrade,'ltc',par)

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
	  continue
	    
      alg(okCoinTrade,'ltc',par)
  except:
      if okCoinTrade:
	del okCoinTrade
	
      print("-----------------------New-----------------------")
      continue
'''
