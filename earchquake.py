# earthquake.py
# import logger  # 日志,单例模式：logger.logger

import numpy as np
import os
import os.path
import zipfile
import sys
import io
import operator
import pandas as pd
from datetime import datetime
import matplotlib as mpl
from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from math import sin, asin, cos, radians, fabs, sqrt
from datetime import datetime

# from datetime import timedelta

# -----------------------------------------------
VERSION = '0.01'
CATALOG_FILE = '5plusEarthQuake.xls'
STATION_CATALOG_FILE = 'catalog_data.csv'
STATION_INFO_FILE = 'station.xls'
EARTH_RADIUS = 6371  # 地球平均半径，6371km


# -----------------------------------------------
class EarthQuake(object):
    # args: txtzip: txt格式的压缩文件，todir：csv格式的压缩文件目录
    def __init__(self, station='53001', start_year=2011,
                 n_years=1):  # ,catalogue_file='',,starttime ='2011-01-01',endtime='2012-12-31'
        # 日志
        print('__init__EarthQuake', station, start_year, n_years)
        # self.log = logger.logger
        # 站点
        self.station = station
        self.station_x = None
        self.station_y = None
        # 时间段
        self.start_year = start_year
        self.n_years = n_years
        # self.starttime = starttime#datetime.strptime(starttime,'%Y-%m-%d')
        # self.endtime = endtime#datetime.strptime(endtime,'%Y-%m-%d')
        # 最终地震目录数据
        self.catalog_data = None
        # 站点地震目录文件名
        self.station_catalog_file = os.getcwd() + os.path.sep + self.station + '_' + STATION_CATALOG_FILE
        # ------------------
        # 初始化站点经纬度
        station_info_file = os.getcwd() + os.path.sep + STATION_INFO_FILE
        head_name = [r'台站名称', r'台站代码', r'所属区域', r'经度', r'纬度', r'高程', r'详细']
        station_info_pd = pd.read_excel(station_info_file, sheetname=0, header=2)  # ,names=head_name
        station_info_pd.columns = head_name
        # print(station_info_pd)
        try:
            # print('台站代码列:',station_info_pd[r'台站代码'])
            print(station_info_pd[station_info_pd[r'台站代码'] == int(self.station)])  # '台站:',S
            self.station_x = station_info_pd[station_info_pd[r'台站代码'] == int(self.station)][r'经度']
            self.station_y = station_info_pd[station_info_pd[r'台站代码'] == int(self.station)][r'纬度']
            print(self.station, '的经度纬度:', float(self.station_x), float(self.station_y))
        except:
            print('没有该站点:', self.station)
            # self.log.error('没有该站点')
            return None
        self.catalog_data_pd = None
        self.catalog_distance_pd = None

    # ----------
    # 初始化地震目录数据
    def init_catalog(self):
        catalog_data_file = os.getcwd() + os.path.sep + CATALOG_FILE
        head_nm = [r'日期', r'时间', r'纬度', r'经度', r'深度', r'Ms', r'mB参考地点']  # ,r'发震时间'
        self.catalog_data_pd = pd.read_excel(catalog_data_file, sheet_name=1, header=1,
                                             index_col=2)  # ,names=head_name self.catalog_
        self.catalog_data_pd.columns = head_nm  # self.catalog_
        self.catalog_data_pd.sort_index(inplace=True)
        # print(self.catalog_data_pd.head())
        # print(self.starttime,data_pd[self.starttime])
        # self.catalog_data_pd = data_pd[self.starttime:self.endtime]
        # self.catalog_data_pd = data_pd[datetime.strptime(data_pd.index,'%Y-%m-%d %H:%M:%S')-self.starttime>=0 and datetime.strptime(data_pd.index,'%Y-%m-%d %H:%M:%S')-self.endtime<=0]
        # print(self.catalog_data_pd.tail())

    # 获取距离站点distance距离的所有地震(distance公里)并只选取给定的时间段内的地震
    def select_catalog_by_distance(self, distance):
        self.catalog_data_pd['distance'] = list(
            map(lambda x, y: self.geodistance_station(x, y), self.catalog_data_pd[r'经度'], self.catalog_data_pd[r'纬度']))
        # self.catalog_data_pd.assign(distance = self.geodistance_station(self.catalog_data_pd[r'经度'],self.catalog_data_pd[r'纬度']))
        # print('catalog_data_pd head:',self.catalog_data_pd['distance'].head())
        distance_pd = self.catalog_data_pd[self.catalog_data_pd['distance'] < distance]
        print('distance_pd head:', distance_pd.head())
        print('self.start_year:', self.start_year)
        '''for index,row in distance_pd.iterrows():
            print(index,row)
            print('index.year',index.year)
            break'''
        year_list = [self.start_year]
        for n in range(1, self.n_years):
            year_list.append(self.start_year + n)
        print(year_list)
        distance_pd_temp = distance_pd[distance_pd.index.year.isin(
            year_list)]  # distance_pd.index.year == self.start_year and distance_pd.index.year <self.start_year+self.n_years]
        '''if self.n_years > 1 :
            for n in range(1,self.n_years):
               distance_pd_temp =  pd.concat([distance_pd_temp,distance_pd[distance_pd.index.year == self.start_year+n]])'''
        self.catalog_distance_pd = distance_pd_temp
        # distance_pd1 = distance_pd[distance_pd.index.year == self.start_year]
        # distance_pd2 = distance_pd[distance_pd.index.year == self.start_year+1]
        # self.catalog_distance_pd = pd.concat([distance_pd[distance_pd.index.year == self.start_year],distance_pd[distance_pd.index.year == self.start_year+1]])#distance_pd[distance_pd.index.year == self.start_year+1]
        # self.catalog_distance_pd.append(distance_pd[distance_pd.index.year == (self.start_year+2)])  #= distance_pd[distance_pd.index.year == self.start_year]
        # catalog_distance_pd = [self.geodistance_station(row[r'经度'],row[r'纬度']<distance ) for row in self.catalog_data_pd.iterrows() ]
        # print('head:',catalog_distance_pd.head())#catalog_distance_pd
        print('self.catalog_distance_pd:', self.catalog_distance_pd)
        return self.catalog_distance_pd

    def hav(self, theta):
        s = sin(theta / 2)
        return s * s

    def station_distance_hav(self, lat1, lng1):
        "用haversine公式计算球面两点间的距离。"
        # 经纬度转换成弧度
        lat0 = radians(self.station_x)
        lat1 = radians(self.station_y)
        lng0 = radians(lng0)
        lng1 = radians(lng1)

        dlng = fabs(lng0 - lng1)
        dlat = fabs(lat0 - lat1)
        h = self.hav(dlat) + cos(lat0) * cos(lat1) * self.hav(dlng)
        distance = 2 * EARTH_RADIUS * asin(sqrt(h))

        return distance

    # 计算两点间距离--公里#-m
    def geodistance(lng1, lat1, lng2, lat2):
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * EARTH_RADIUS  # *1000
        return dis

    def geodistance_station(self, lng, lat):
        lng1, lat1, lng2, lat2 = map(radians, [self.station_x, self.station_y, lng, lat])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * EARTH_RADIUS  # *1000
        return dis

    # 绘图
    def draw_by_distance(self, ax, distance):
        # print('init_catalog...')
        # self.init_catalog()
        print('select_catalog_by_distance...')
        self.catalog_distance_pd = self.select_catalog_by_distance(distance)
        ax1 = ax
        # ax1.title('站点:%s附近地震情况'%self.station)
        # ax1.title('站点')
        # ax1.set_xlabel('发震时间')
        ax1.set_xlabel('发震时间(站点:%s)' % self.station)
        ax1.set_ylabel('距离(公里)o')
        ax2 = ax1.twinx()
        ax2.set_ylim(0.0, 10.0)
        ax2.set_ylabel('震级*')
        ax1.plot(self.catalog_distance_pd['distance'], 'ro')
        ax2.plot(self.catalog_distance_pd['Ms'], 'y*')
        # ax1.annotate('%s'%self.catalog_distance_pd[r'mB参考地点'],self.catalog_distance_pd['Ms'],self.catalog_distance_pd['Ms']+0.5)
        for index, row in self.catalog_distance_pd.iterrows():
            ax1.axvline(index)
            # print(index.year)
            ax2.annotate('%s' % row[r'mB参考地点'], xy=(index, row['Ms']), xytext=(index, row['Ms'] + 0.2))

        # self.catalog_distance_pd.plot(style='.--',ax=ax1)

    def draw_default(self, ax):
        ax1 = ax
        ax1.set_xlabel('发震时间(站点:%s)' % self.station)
        ax1.set_ylabel('距离(公里)o')
        ax2 = ax1.twinx()
        ax2.set_ylim(0.0, 10.0)
        ax2.set_ylabel('震级*')
        ax1.plot(self.catalog_distance_pd['distance'], 'y*')
        ax2.plot(self.catalog_distance_pd['Ms'], 'ro')
        for index, row in self.catalog_distance_pd.iterrows():
            ax1.axvline(index)
            ax2.annotate('%s' % row[r'mB参考地点'], xy=(index, row['Ms']), xytext=(index, row['Ms'] + 0.2))


if __name__ == "__main__":
    eq1 = EarthQuake(station='53001', start_year=2011,
                     n_years=2)  # EarthQuake(station='53001',starttime ='2011-01-01',endtime='2016-12-31')
    # ----test1----
    # eq2 = EarthQuake(station='53095')
    # dis = eq1.geodistance_station(eq2.station_x,eq2.station_y )
    # print(eq1.station,eq2.station,'的距离',dis)
    # -----test2--
    print('init_catalog...')
    eq1.init_catalog()
    # print('select_catalog_by_distance...')
    # catalog_distance_pd = eq1.select_catalog_by_distance(500)
    # print("-----------------------")
    # print('catalog_distance_pd:\n',catalog_distance_pd)
    # print('tail:',catalog_distance_pd.tail())
    # 解决中文的问题
    mpl.use('TkAgg')
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.family'] = 'sans-serif'
    # 解决负号'-'显示为方块的问题
    mpl.rcParams['axes.unicode_minus'] = False

    width = 10
    height = 8

    fig = plt.figure(figsize=(width, height), dpi=100)
    ax1 = fig.add_subplot(111)
    eq1.draw_by_distance(ax1, 500)
    '''ax1.set_xlabel('发震时间')
    ax1.set_ylabel('距离(公里)')
    ax2 = ax1.twinx()
    ax2.set_ylim(0.0,10.0)
    ax2.set_ylabel('震级')
    #x = range(len(catalog_distance_pd['distance']))
    #ax1.bar(left = x,height=catalog_distance_pd['distance'], width=0.4, alpha=0.8, color='red', label="距离")
    #ax1.plot(catalog_distance_pd['日期'],catalog_distance_pd['distance'],'ro')#,style='.--',ax=ax1
    ax1.plot(catalog_distance_pd['distance'],'y*')    
    ax2.plot(catalog_distance_pd['Ms'],'ro')
    #ax1.set_xticks('发震时间')
    #plt.legend()
    #ax1.axvline(catalog_distance_pd.index)
    #catalog_distance_pd['zero'] = 0#list(map(lambda x :x-x,catalog_distance_pd['Ms']))
    #print(catalog_distance_pd.head())
    for index,row in  catalog_distance_pd.iterrows():
        #print(row['Ms'])
        #print(row['日期'],row['Ms'],index,row['distance'],row['mB参考地点'])#row['发震时间']
        ax1.axvline(index)
        #ax1.plot(row['Ms'],row['zero'],'r-')
        #ax1.plot((index,row['zero']),(index,row['Ms']) ,'r-')#row['日期'],row['日期'],style='-'
        #break
    print("-----------------------")
    '''
    # ax1.xticks([index + 0.2 for index in x], catalog_distance_pd['日期'])
    # catalog_distance_pd['distance'].plot(style='.--',ax=ax1)
    # path,filename = os.path.split(tstc.txt)
    # tstc.drawOutlierLine(ax1,pic_name=filename,lose=r'NAN',out_base=2)
    # tstc.drawDateline(ax1,pic_name = filename,ktype = 'month',lose=r'NAN')#drawDateline(self,ax,pic_name='',ktype = 'day',lose='')
    # tstc.drawKline(ax1,pic_name=filename,ktype = 'month',lose=r'NAN')#drawKline(self,ax,pic_name='',ktype = 'day',lose='')
    plt.show()
