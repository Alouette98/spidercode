import requests
import re
import json
import csv
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import *
from bs4 import BeautifulSoup
from requests.packages import urllib3
from fake_useragent import UserAgent
from retrying import retry

urllib3.disable_warnings()

class Spider:
	"""docstring for Spider"""

	def __init__(self,name,userid):
		self.name = name
		self.id = userid
		self.counter = 0
		self.retrycounter = 0

	def genurl(self):
		# 这里是表层网页
		return "http://www.toubang.tv/anchor/1_"+str(self.id)+".html"

	def genurl7(self):
		# 这里是7日数据
		return "http://www.toubang.tv/anchor/ajax/getinfo?pt=1&rid="+str(self.id)+"&dt=7&date=0"

	def genurl1(self):
		# 这里是昨日数据
		return "http://www.toubang.tv/anchor/ajax/getinfo?pt=1&rid="+str(self.id)+"&dt=1&date=0"

	def decode(self,soupObject):

		for item in soupObject:
			result = item.get_text()	

		if str.isdigit(result):
			return int(result)
		elif "分类" in result:
			return ' '.join(result.strip().split()).replace(" ",",").replace("分类,","")
		else:
			return result


	@retry(stop_max_attempt_number=5, wait_random_min=500, wait_random_max=1000)
	def getData(self):

		ua = UserAgent()
		headers = {'User-Agent':ua.random}
		
		url = self.genurl()
		url7 = self.genurl7()
		url1 = self.genurl1()

		response = requests.get(url,headers = headers,verify = False,timeout=5)
			
		time.sleep(random.uniform(0.05,0.85))

		response7day = requests.get(url7,headers = headers,verify = False,timeout=5)
		
		time.sleep(random.uniform(0.05,0.85))

		response1day = requests.get(url1,headers = headers,verify = False,timeout=5)
		
		soup = BeautifulSoup(response.text,'lxml')


		if self.retrycounter >= 4:
			print('>>> 主播网页异常！主播已退出公会，或者头榜服务器异常')
			return [self.name,self.id, "【该主播已退出公会，或网页异常】",0,0,0,0,0,0]

		try:
			## 服务器开小差、或者关注人数那里不存在（即退出公会）时，这里会报错，然后触发重试机制。
			## 如果重试超过4次，则认为的确不存在，而不是短暂的网页获取失败。
			followerNum = self.decode(soup.select('body > div > div.host-header > div > div > div > div.zhubo-info.fl.mt40 > div > div.i-txt.fl > dl:nth-child(6) > dd > span.color-yello.mr10'))
		except:
			self.retrycounter = self.retrycounter + 1
			raise TypeError('') from E


		############ 如果网页正常 ############
		
		### 成功获得网页次数 self.counter 
		self.counter = self.counter + 1
		
		try:
			data_1day = response1day.json()
		except:
			print(">>> 昨日数据获取失败。该主播昨日可能没有上播。付费礼物、弹幕数将设置为0。")
			totalBarage = 0
			paidPresent = 0
		else:
			totalBarage = data_1day['msgNum']		    # 总弹幕数
			paidPresent = data_1day['giftWorth']/100    # 付费礼物



		district = self.decode(soup.select('body > div > div.host-header > div > div > div > div.zhubo-info.fl.mt40 > div > div.i-txt.fl > dl:nth-child(4) > dd'))
		try:
			data_7day = response7day.json()
		except:
			print(">>> 近7天数据获取失败。该主播上周可能没有上播。日均活跃,潜力值和实力值将设置为0。")
			avgDailyActive = 0
			potential = 0
			strength = 0
		else:
			followerNum = data_7day['fans']
			potential = data_7day['potential']           # 潜力值
			strength = data_7day['score']                # 实力值
			if followerNum == 0:
				followerNum = self.decode(soup.select('body > div > div.host-header > div > div > div > div.zhubo-info.fl.mt40 > div > div.i-txt.fl > dl:nth-child(6) > dd > span.color-yello.mr10'))
			avgDailyActive = data_7day['avgInteractNum']   

		if self.counter >=4:
			print('>>> 主播网页异常！主播已退出公会，或者头榜服务器异常')
			return [self.name,self.id, "【该主播已退出公会，或网页异常】",0,0,0,0,0,0]
		else:
		# print([self.name,self.id, district,followerNum,avgDailyActive,totalBarage,paidPresent,potential,strength])
			return [self.name,self.id, district,followerNum,avgDailyActive,totalBarage,paidPresent,potential,strength]
