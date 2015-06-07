# -*- coding: utf-8 -*-
#邮箱
email    = "489509928@qq.com"
#密码
password = "lan@2014"

      #浏览器重新登录间隔，值越大间隔越久，为防止卡死
par={ 'numReLogin'   :30, 
      #记录数据的最大条数
      'maxNum'       :100,  
      #记录数据的最小条数
      'minNum'       :50,    
      #记录数据时间间隔（单位秒）
      'recordTime'   :5,
      #单次交易虚拟币数量
      'amount'       :0.1,
      #两次自动交易的时间间隔
      'deltaTime'    :2     } 

#------------------------
# 在此选择所需要的算法
from algorithm_5 import *
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
	  continue

      alg(okCoinTrade,'ltc',par)      
    except:
      if okCoinTrade:
	del okCoinTrade
	
      print("-----------------------New-----------------------")
      continue
	
    
