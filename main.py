# 导入运行必要的代码仓库
import lib.spider

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



filePath = './database/name_with_id.csv'
f = csv.reader(open(filePath,"r",encoding='UTF-8-sig'))
counter = 0
output = []
title = ['主播名','主播房间号','所在版块','关注订阅','日均活跃观众','弹幕总数','付费礼物','潜力值','实力值']

for i in f:
	counter = counter + 1
	print("正在获取第", counter, "个主播,主播名为【",i[0],"】。\t")
	a = lib.spider.Spider(i[0],i[1])
	try:
		output.append(a.getData())
	except:
		output.append([a.name,a.id,'【未知错误】',0,0,0,0,0,0])
		
csv_df = pd.DataFrame(columns = title, data = output)
timenow = time.strftime("%Y%m%d_%H%M%S", time.localtime())

print("\n>>> 生成csv文件中……")
csv_df.to_csv('./csvfiles/'+timenow+'.csv',encoding='UTF-8-sig')

print(">>> 生成可视化图中……")
matplotlib.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.sans-serif']='SimHei'

paid_present = csv_df[['主播名','付费礼物']]
myfont = FontProperties(fname='./fonts/simsun.ttc')
matplotlib.rcParams['axes.unicode_minus']=False
paid_present_pivot = pd.pivot_table(paid_present, values='付费礼物', index='主播名', aggfunc='sum').reset_index().sort_values(ascending=True,by='付费礼物')
f, ax = plt.subplots(figsize=(16,12/40*counter))
barh = plt.barh(paid_present_pivot['主播名'].values, paid_present_pivot['付费礼物'].values,
                color='dodgerblue')
barh[-1].set_color('gold')
barh[-2].set_color('silver')
barh[-3].set_color('orange')
for y, x in enumerate(paid_present_pivot['付费礼物'].values):
    plt.text(x+50, y-0.2, "%s" %x)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tick_params(labelsize=14)
plt.xlabel('付费礼物',fontproperties = myfont)
plt.ylabel('主播名',fontproperties = myfont)
plt.title('各主播付费礼物',fontproperties = myfont,fontSize = 24)
f.savefig('./img/付费礼物_'+timenow+'.png',bbox_inches = 'tight')

paid_present = csv_df[['主播名','弹幕总数']]
myfont = FontProperties(fname='./fonts/simsun.ttc')
matplotlib.rcParams['axes.unicode_minus']=False
paid_present_pivot = pd.pivot_table(paid_present, values='弹幕总数', index='主播名', aggfunc='sum').reset_index().sort_values(ascending=True,by='弹幕总数')
f, ax = plt.subplots(figsize=(16,12/40*counter))
barh = plt.barh(paid_present_pivot['主播名'].values, paid_present_pivot['弹幕总数'].values,
                color='dodgerblue')
barh[-1].set_color('gold')
barh[-2].set_color('silver')
barh[-3].set_color('orange')
for y, x in enumerate(paid_present_pivot['弹幕总数'].values):
    plt.text(x+50, y-0.2, "%s" %x)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tick_params(labelsize=14)
plt.xlabel('弹幕总数',fontproperties = myfont)
plt.ylabel('主播名',fontproperties = myfont)
plt.title('各主播弹幕总数',fontproperties = myfont,fontSize = 24)
f.savefig('./img/弹幕总数_'+timenow+'.png',bbox_inches = 'tight')

print(">>> 生成完毕，程序结束！请到csvfiles和img文件夹下查看csv和图表。 数据如有异常请再次运行本程序。")


	