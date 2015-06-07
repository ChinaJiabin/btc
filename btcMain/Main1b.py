# -*- coding: utf-8 -*-
#帐号
partner   = 
#密钥 
secretKey = ''

      #交易虚拟币类型（比特币或莱特币）
par={ 'typeTc'           :'ltc',
      #浏览器重新登录间隔，值越大间隔越久，为防止卡死
      'numReLogin'       :10,

      #当前价高于买入均价_多少 则全卖出（单位:元）
      'deltaAPrice'      :0.01,
      #当前价高于基准价_多少 则全卖出（单位:元）
      'deltaBPrice'      :0.01,

      #单笔买交易基准数量
      'baseAmount'       :0,  
      #单笔买交易递增数量
      'deltaAmount'      :0.1, 
   
      #获取当前价的时间间隔（单位:秒）      
      'updateTime'       :5,
      #插入第一笔买事件的最长等待时间（单位：秒）
      'waitTime'         :3*60,
      #两笔买交易发生的最短时间间隔（单位:秒）
      'deltaTime'        :2*60 } 
  
#------------------------
# 在此选择所需要的算法
from alg1b import *
#------------------------

okCoinTrade = okCoin( par['typeTc'], partner, secretKey )
alg(okCoinTrade,par)


