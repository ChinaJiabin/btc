# -*- coding: utf-8 -*-
import urllib2
import threading
import re
import time
import datetime
from splinter import *

class obtainData:
    def __init__(self):
        #---------------------------------------------------------------------
        #okCoin网站地图
        self.url={'btcData':"https://www.okcoin.cn/market.do?symbol=0", 
                  'ltcData':"https://www.okcoin.cn/market.do?symbol=1", 

                  'btcBuy' :"https://www.okcoin.cn/trade/btc.do?tradeType=0",
                  'btcSell':"https://www.okcoin.cn/trade/btc.do?tradeType=1",
                  'ltcBuy' :"https://www.okcoin.cn/trade/ltc.do?tradeType=0",
                  'ltcSell':"https://www.okcoin.cn/trade/ltc.do?tradeType=1",
                 
                  'login'  :"http://www.okcoin.cn",
                  'record' :'https://www.okcoin.cn/account/record.do'}
        #---------------------------------------------------------------------
        #正则表达式
        self.reg={'buyPrice'    :'<span id="buyPriceSpan\d+">([0-9,]+.[0-9]+|[0-9,]+)',
                  'sellPrice'   :'<span id="sellPriceSpan\d+">([0-9,]+.[0-9]+|[0-9,]+)', 
                  'btcLatestPrice' :'id="bannerBtcLast" class="\w+">([0-9,]+.[0-9]+|[0-9,]+)',
                  'ltcLatestPrice' :'id="bannerLtcLast" class="\w+">([0-9,]+.[0-9]+|[0-9,]+)',
                  
                  'btcBuyAmount'   :'<span id="buyAmountSpan\d+">฿([0-9,]+.[0-9]+|[0-9,]+)',
                  'btcSellAmount'  :'<span id="sellAmountSpan\d+">฿([0-9,]+.[0-9]+|[0-9,]+)',
                  'ltcBuyAmount'   :'<span id="buyAmountSpan\d+">Ł([0-9,]+.[0-9]+|[0-9,]+)',        
                  'ltcSellAmount'  :'<span id="sellAmountSpan\d+">Ł([0-9,]+.[0-9]+|[0-9,]+)',

                  'CNYGet'         :'CNY:</span><span class="money \w+">([0-9,]+.[0-9]+|[0-9,]+)',
                  'ltcGet'         :'LTC:</span><span class="money \w+">([0-9,]+.[0-9]+|[0-9,]+)',
                  'btcGet'         :'BTC:</span><span class="money \w+">([0-9,]+.[0-9]+|[0-9,]+)'}        
        #---------------------------------------------------------------------
        self.buyPrice    ={'btc':[],'ltc':[]}
        self.buyAmount   ={'btc':[],'ltc':[]}
        self.sellPrice   ={'btc':[],'ltc':[]}
        self.sellAmount  ={'btc':[],'ltc':[]}

        self.latestPrice ={'btc':0,'ltc':0}
        #---------------------------------------------------------------------
        
    def update(self,name,isAllUpdate=False):
        while 1:
          try:
            f = urllib2.urlopen(self.url[name+'Data'],timeout=10).read()
            break
          except:
            time.sleep(5)

        if isAllUpdate:
           self.buyPrice[name]  =[float( x.replace(',','') ) for x in re.findall(self.reg['buyPrice'],f)]
           self.sellPrice[name] =[float( x.replace(',','') ) for x in re.findall(self.reg['sellPrice'],f)]
           self.buyAmount[name] =[float( x.replace(',','') ) for x in re.findall(self.reg[name+'BuyAmount'],f)]
           self.sellAmount[name]=[float( x.replace(',','') ) for x in re.findall(self.reg[name+'SellAmount'],f)]
        temp =re.findall(self.reg[name+'LatestPrice'],f)
        self.latestPrice[name]=float( temp[0].replace(',','') )
       
    def averagePrice(self,num,typeDeal,typeTc):
        price   = 0
        amount  = 0
        self.update(typeTc,True)
        if typeDeal=='Buy':
           for i in range(num):
               price +=self.buyPrice[typeTc][i]*self.buyAmount[typeTc][i]
               amount+=self.buyAmount[typeTc][i]
        if typeDeal=='Sell':
           for i in range(num):
               price +=self.sellPrice[typeTc][i]*self.sellAmount[typeTc][i]
               amount+=self.sellAmount[typeTc][i]
        return round(price*1.0/amount,3)       
   
class autoTrade(obtainData):
    def __init__(self,email,password):
        obtainData.__init__(self)
        #---------------------------------------------------------------------
        #登陆okCoin网站
        self.loginEmail   =email
        self.loginPassword=password
        
        self.browser=Browser()
        self.browser.visit(self.url['login'])
        self.browser.find_by_id('indexLoginName').fill(self.loginEmail)    
        self.browser.find_by_id('indexLoginPwd').fill(self.loginPassword)             
        self.browser.execute_script("loginIndexSubmit()")
        #---------------------------------------------------------------------
        
    def __del__(self):
        self.browser.quit()

    def getAccount(self,typeSet):
        while 1:
           html = self.browser.html
           Tc   = re.findall(self.reg[typeSet+'Get'],html)
           if Tc:
              return float( Tc[0].replace(',','') )

    def reLogin(self,typeDeal=None):
        self.browser.quit()
        self.browser = Browser()
        self.browser.visit(self.url['login'])
        self.browser.find_by_id('indexLoginName').fill(self.loginEmail)    
        self.browser.find_by_id('indexLoginPwd').fill(self.loginPassword)             
        self.browser.execute_script("loginIndexSubmit()")
        if typeDeal:
           self.browser.visit(self.url[typeDeal])
    
    def queueAdd(self,typeTc,price,amount):
        while 1:
          try:
             self.browser.visit(self.url[typeTc])
             self.browser.find_by_id('tradeCnyPrice').fill(price)
             self.browser.find_by_id('tradeAmount').fill(amount)
             self.browser.execute_script('submitTradeBtcForm()') 
             break
          except:
              self.reLogin()
