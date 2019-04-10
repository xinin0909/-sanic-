# txt2static.py
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
from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from zfile import ZFile
import kplot

TXT2STATIC_VERSION = '1.0'  # 优化了获取数据


class Txt2Static(object):
    # args: txtzip: txt格式的压缩文件，todir：csv格式的压缩文件目录
    def __init__(self, txt='', todir=''):
        print('Txt2Static init...')
        # self.log = logger.logger
        self.txt = txt
        # path,zipfile = os.path.split(self.txtzip)
        # self.zipfile = zipfile
        # todir:
        self.todir = todir
        if not self.todir or len(self.todir) < 3:
            self.todir = os.getcwd() + os.path.sep + 'csv'
        else:
            pass
        if not os.path.exists(self.todir):
            os.makedirs(self.todir)
        self.tmpdir = self.todir  # os.getcwd() + os.path.sep +'tmp'#临时目录
        # if not os.path.exists(self.tmpdir):
        #    os.makedirs(self.tmpdir)

    # ------------------------------------------------------
    def drawKline(self, ax, pic_name='', ktype='day', lose=''):  # u'分析图'
        if (not self.txt) or len(self.txt) < 3:
            self.log.error('self.txt为空:' + self.txt)
            return None
        txt = self.txt
        csvpd = self.getCsvpd(txt, lose)
        klinepd = self.getKline(csvpd, ktype)
        # print("day end")
        # print(klineday.dtypes)
        # klinepd.to_csv(dayfile, header=None)#index_col=0,,sep=' ',names=['d','v']
        if pic_name == '':
            path, filename = os.path.split(self.txt)
            name = filename
        else:
            name = pic_name
        kplot.KplotByAx(ax, name, klinepd['mean'], klinepd['max'], klinepd['min'], klinepd['median'])
        path, filename = os.path.split(self.txt)
        name, ext = os.path.splitext(filename)
        csv = self.tmpdir + os.path.sep + name + ".csv"
        klinepd.to_csv(csv, header=None)
        # print(dayfile)
        # print(klinepd.dtypes)
        return csv

    def drawLine(self, ax, pic_name='', lose=''):  # u'分析图'
        if (not self.txt) or len(self.txt) < 3:
            # self.log.error('self.txt为空:' + self.txt)
            return None
        txt = self.txt
        csvpd = self.getCsvpdDates(txt, lose)
        print(csvpd.head())
        ax1 = ax  # fig.add_subplot(111)
        ax1.plot(csvpd, 'b.', label='original data')
        # for index,row in  csvpd.iterrows():
        # ax1.scatter(index,row['v'],c='b',marker = '*')
        # print(index,row['v'])
        # csvpd.plot(style='ko--',ax=ax1,label='original data')
        # ax1. scatter(csvpd.index,csvpd['v'],c='r',marker='*',label='original data')
        if pic_name == '':
            path, filename = os.path.split(self.txt)
            pic_name = filename
        else:
            pic_name = pic_name
        ax1.set_title(pic_name)
        ax1.legend()
        path, filename = os.path.split(self.txt)
        name, ext = os.path.splitext(filename)
        csv = self.tmpdir + os.path.sep + name + ".csv"
        csvpd.to_csv(csv, header=None)
        return csv

    def drawOutlierLine(self, ax, pic_name='', lose='', out_base=2):  # u'分析图'
        if (not self.txt) or len(self.txt) < 3:
            # self.log.error('self.txt为空:' + self.txt)
            return None
        txt = self.txt
        outlpd = self.getCsvpdOutlier(txt, lose, out_base)  # getCsvpdOutlier getCsvpdDates
        print(outlpd.head())
        ax1 = ax  # fig.add_subplot(111)
        # md = outlpd.v.median()
        outlpd.plot(style='rD', ax=ax1, label='outlier data')  # --
        # outlpd.plot(kind='scatter',c='r',marker='D',label='outlier data')
        # for indexs in outlpd.index:
        #    ax1.scatter(indexs,outlpd.loc[indexs].values[-1],c='r',marker='D',label='outlier data')
        # ax1.scatter(outlpd['d'],outlpd['v'],c='r',marker='D',label='outlier data')
        '''for indexs in outlpd.index:
            if outlpd.loc[indexs].values[-1]>3*md:
                ax1.scatter(indexs,outlpd.loc[indexs].values[-1],c='r',marker='D',label='outlier data')
            else:
                ax1.scatter(indexs,outlpd.loc[indexs].values[-1],c='b',marker='*',label='outlier data')'''
        if pic_name == '':
            path, filename = os.path.split(self.txt)
            pic_name = filename
        else:
            pic_name = pic_name
        ax1.set_title(pic_name)
        # ax1.legend()
        path, filename = os.path.split(self.txt)
        name, ext = os.path.splitext(filename)
        csv = self.tmpdir + os.path.sep + name + ".csv"
        outlpd.to_csv(csv, header=None)
        return csv

    def drawDateline(self, ax, pic_name='', ktype='day', lose=''):  # u'分析图'
        if (not self.txt) or len(self.txt) < 3:
            # self.log.error('self.txt为空:' + self.txt)
            return None
        txt = self.txt
        csvpd = self.getCsvpd(txt, lose)
        print('original data:', csvpd.head())
        klinepd = self.getKline(csvpd, ktype)
        # print('%s type data'%ktype,klinepd.head())
        ax1 = ax  # fig.add_subplot(111)
        # klinepd.plot.scatter(0,0,ax=ax1)
        # ax1.plot(klinepd)#.mean klinepd.day,columns=['mean','median data','max data','min data']
        # ax1.plot(klinepd.median,label='median data')
        # ax1.plot(klinepd.max,label='max data')
        # ax1.plot(klinepd.min,label='min data')
        # ax1.scatter(klinepd,c='r',marker='*')#,label='original data'
        if ktype == 'day':
            klinepd.plot(style='.--', ax=ax1)  # --
        else:
            klinepd.plot(style='o--', ax=ax1)
        if pic_name == '':
            path, filename = os.path.split(self.txt)
            pic_name = filename
        else:
            pic_name = pic_name
        ax1.set_title(pic_name)
        ax1.legend()
        path, filename = os.path.split(self.txt)
        name, ext = os.path.splitext(filename)
        csv = self.tmpdir + os.path.sep + name + ".csv"
        klinepd.to_csv(csv, header=None)
        return csv

    # ----------------------------------------
    def getCsvpd(self, txt, lose=''):
        if isinstance(txt, bytes):
            txt = str(txt)
        # dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H%M')
        csvpd = pd.read_table(txt, index_col=0, header=None, sep=' ',
                              names=['d', 'v'])  # ,parse_dates=[0],date_parser=dateparse
        # print(csvpd.head())
        # print(csvpd.describe())
        # csvpd_ok = csvpd[csvpd.v<99999.0]#.copy()
        if (lose == r'Median'):
            csvpd_ok = csvpd[csvpd.v < 99999.0]
            md = csvpd_ok.v.median()
            csvpd[csvpd.v > 99999.0] = md
        elif (lose == r'Mean'):
            csvpd_ok = csvpd[csvpd.v < 99999.0]
            mn = csvpd_ok.v.mean()
            csvpd[csvpd.v > 99999.0] = mn
            # elif(lose == r'Last'):
            #    self.txt2csvLast(txt,csv)
        elif (lose == r'Zero'):
            csvpd[csvpd.v > 99999.0] = 0
        elif (lose == r'NAN'):
            csvpd[csvpd.v > 99999.0] = np.nan
        else:
            pass
        #
        '''md = csvpd_ok.v.median()
        std = csvpd_ok.v.std()
        if(csvpd.v.max()>3*std and csvpd.v.max()>4*md):                    
                        csvpd[csvpd.v>3*std] = 4*md'''
        return csvpd

    def getCsvpdDates(self, txt, lose=''):
        if isinstance(txt, bytes):
            txt = str(txt)
        pdtest = pd.read_table(txt, index_col=0, header=None, sep=' ', names=['d', 'v'], nrows=5)
        for d, v in pdtest.iterrows():
            n = len(str(d))
            # print(d,v,n)
            if n == 6:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m')
            elif n == 8:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
            elif n == 10:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H')
            elif n == 12:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H%M')
            else:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H%M')
            break
        pdtest = None
        print('get timestamp format ok.')
        csvpd = pd.read_table(txt, index_col=0, header=None, sep=' ', names=['d', 'v'], parse_dates=[0],
                              date_parser=dateparse)  #
        print('gread_table %s ok.' % txt)
        # print(csvpd.describe())
        csvpd_ok = csvpd[csvpd.v < 99999.0]  # .copy()
        if (lose == r'Median'):
            md = csvpd_ok.v.median()
            csvpd[csvpd.v > 99999.0] = md
        elif (lose == r'Mean'):
            mn = csvpd_ok.v.mean()
            csvpd[csvpd.v > 99999.0] = mn
            # elif(lose == r'Last'):
            #    self.txt2csvLast(txt,csv)
        elif (lose == r'Zero'):
            csvpd[csvpd.v > 99999.0] = 0
        elif (lose == r'NAN'):
            csvpd[csvpd.v > 99999.0] = np.nan
        else:
            pass
        #
        '''md = csvpd_ok.v.median()
        std = csvpd_ok.v.std()
        #if(csvpd.v.max()>3*std and csvpd.v.max()>4*md):                    
        csvpd[csvpd.v>3*std] = 4*md'''
        return csvpd

    def getCsvpdOutlier(self, txt, lose='', out_base=2):
        if isinstance(txt, bytes):
            txt = str(txt)
        pdtest = pd.read_table(txt, index_col=0, header=None, sep=' ', names=['d', 'v'], nrows=5)
        for d, v in pdtest.iterrows():
            n = len(str(d))
            if n == 6:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m')
            elif n == 8:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
            elif n == 10:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H')
            elif n == 12:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H%M')
            else:
                dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d%H%M')
            break
        pdtest = None
        csvpd = pd.read_table(txt, index_col=0, header=None, sep=' ', names=['d', 'v'], parse_dates=[0],
                              date_parser=dateparse)  #
        # print(csvpd.head())
        # print(csvpd.describe())
        csvpd_ok = csvpd[csvpd.v < 99999.0]  # .copy()
        if (lose == r'Median'):
            md = csvpd_ok.v.median()
            csvpd[csvpd.v > 99999.0] = md
        elif (lose == r'Mean'):
            mn = csvpd_ok.v.mean()
            csvpd[csvpd.v > 99999.0] = mn
            # elif(lose == r'Last'):
            #    self.txt2csvLast(txt,csv)
        elif (lose == r'Zero'):
            csvpd[csvpd.v > 99999.0] = 0
        elif (lose == r'NAN'):
            csvpd[csvpd.v > 99999.0] = np.nan
        else:
            pass
        #
        # md = csvpd_ok.v.median()
        # std = csvpd_ok.v.std()
        # if(csvpd.v.max()>3*std and csvpd.v.max()>4*md):
        # csvpd[csvpd.v<out_base*std] = np.nan #3
        # csvpd[csvpd.v< (out_base+1)*md] = np.nan#4
        md = csvpd_ok.v.median()
        mn = csvpd_ok.v.mean()
        std = csvpd_ok.v.std()
        # var = csvpd_ok.v.var()
        mad = csvpd_ok.v.mad()
        csvpd[abs(csvpd.v - mn) < out_base * std] = np.nan  # 3
        csvpd[abs(csvpd.v - md) < out_base * mad] = np.nan  # 4
        csvpd.rename(columns={'v': 'outlier'}, inplace=True)
        # outlpd = csvpd[csvpd.v>4*md]#3*std
        # print(outlpd.head())
        return csvpd

    def getKline(self, csvpd, ktype='day'):
        if ktype == 'year':
            csvpd['year'] = [str(d)[:4] for d, v in csvpd.iterrows()]
        elif ktype == 'month':
            csvpd['month'] = [str(d)[4:6] for d, v in csvpd.iterrows()]
        elif ktype == 'day':
            csvpd['day'] = [str(d)[4:8] for d, v in csvpd.iterrows()]
        elif ktype == 'hour':
            csvpd['hour'] = [str(d)[4:10] for d, v in csvpd.iterrows()]
        else:
            csvpd['day'] = [str(d)[4:8] for d, v in csvpd.iterrows()]
        for d, v in csvpd.iterrows():
            year = str(d)[:4]
            break
        print(csvpd.tail(12))
        if ktype in ['hour', 'day', 'month', 'year']:
            kline = csvpd['v'].groupby(csvpd[ktype])  # .mean()
        else:
            kline = csvpd['v'].groupby(csvpd['day'])
            print('ktype error:' + ktype + '>>>>>>>>>used day------')
        # print(kline.median().tail())
        # print("max end-----------------")
        klinepd = pd.DataFrame(kline.mean())
        klinepd.rename(columns={'v': 'mean'}, inplace=True)
        klinepd['median'] = kline.median()
        klinepd['max'] = kline.max()
        klinepd['min'] = kline.min()
        # klinepd['year'] = str(year)
        # print("day:")
        print(klinepd.tail(12))
        # kplot.Kplot(klinepd['mean'],klinepd['max'],klinepd['min'],klinepd['median'])
        # plt.plot(klinepd[:4])
        # plt.show()
        return klinepd

    def getDateline(self, csvpd, ktype='day'):
        self.getKline(scsvpd, ktype)
        return klinepd


if __name__ == "__main__":
    tstc = Txt2Static('data/53016_5_4214_dys_2001-01-01_2001-12-31_623564906.txt')
    # tozip.pandasTest()
    # tozip.toCsvzip(r'NAN')
    width = 10
    height = 8
    # fig = Figure(figsize=(width,height), dpi=100)
    # canvas = FigureCanvas(fig)
    fig = plt.figure(figsize=(width, height), dpi=100)
    ax1 = fig.add_subplot(111)
    print('ax1',ax1)
    plt.ylim(0.0, 10000.0)
    path, filename = os.path.split(tstc.txt)
    tstc.drawLine(ax1, lose=r'NAN')
    # tstc.drawDateline(ax1,pic_name=filename,lose=r'NAN')
    # tstc.drawOutlierLine(ax1, pic_name=filename, lose=r'NAN', out_base=2)
    # tstc.drawDateline(ax1,pic_name = filename,ktype = 'month',lose=r'NAN')#drawDateline(self,ax,pic_name='',ktype = 'day',lose='')
    # tstc.drawKline(ax1,pic_name=filename,ktype = 'month',lose=r'NAN')#drawKline(self,ax,pic_name='',ktype = 'day',lose='')
    plt.show()
    # canvas.print_figure('demo.jpg')
    # tozip.toKline('month',r'NAN')

