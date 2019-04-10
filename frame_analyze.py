import matplotlib as mpl
from zfile import ZFile
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os,json
import txt2static as stc #数据分析模块：Txt2Static
import earchquake as earth
import txt2liststatic as lstc
import logger

VIRSION = 0.51
PNG_FILE_NAME='save.png'
INDEX_FILE_NAME = 'dataindex.json'

class Application():
    def __init__(self,filename,distance,pictype):
        self.virsion = VIRSION
        self.station = ''
        self.log = logger.logger
        # 设置距离目录距离
        self.distance = distance
        self.filename = filename
        # 单年
        self.txt = ''
        # 多年
        self.txtlist = []
        self.start_year = 2011
        self.n_years = 1
        self.catalog_distance_pd = None  # 地震数据

        self.pic_filename = ''  # 当前分析图的数据文件
        self.out_base = 2.0
        # 索引
        path = os.getcwd()

        self.indexfile = path + os.path.sep + INDEX_FILE_NAME
        print(self.indexfile)
        self.indexdict = None
        # if os.path.exists(self.indexfile):
        # with open(self.indexfile, 'r') as f:
        #     jsons = f.read()
        #     self.indexdict = json.loads(jsons)
        #     print('load ' + self.indexfile)
        # 绘图画布
        width = 10
        height = 8
        # self.figure = Figure(figsize=(width, height), dpi=100)
        self.figure = plt.figure(figsize=(width, height), dpi=100)
        # self.canvas = None
        # 路径
        self.importdir = ''  # 待导入的ZIP数据的目录，需设置 #path + os.path.sep +'from'
        self.datadir = path + os.path.sep + 'data'  # 导入到的目录
        self.tmpdir = path + os.path.sep + 'tmp'  # 临时目录
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)
        if not os.path.exists(self.tmpdir):
            os.makedirs(self.tmpdir)
        # 解决中文的问题
        mpl.use('TkAgg')
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.family'] = 'sans-serif'
        # # 解决负号'-'显示为方块的问题
        # mpl.rcParams['axes.unicode_minus'] = False
        print(type(filename))
        if type(filename) is str:
            # 设置检查站编号
            self.set_yearfile()
            self.get_distance_earthquake()
            print('set单年')
            if pictype == 'origindraw':
                self.draw()
            elif pictype == 'daydraw':
                self.day_draw()
            elif pictype == 'monthdraw':
                self.month_draw()
            elif pictype == 'month_kdraw':
                self.month_draw_kline()
            # self.show_canvas()
            self.save_pic()
        elif type(filename) is list:
            # 设置检查站编号
            self.txtlist = filename
            self.set_multfile(self.txtlist)
            self.station = '53079'
            self.start_year = 2006
            self.n_years = len(filename)
            self.get_distance_earthquake()
            print('set多年')
            if pictype == 'origindraw':
                self.mult_draw()
            elif pictype == 'monthdraw':
                self.mult_month_draw()
            elif pictype == 'month_kdraw':
                self.mult_month_draw_kline()
            # self.show_canvas()
            self.save_pic()
        else:
            return None


    def get_distance_earthquake(self):#,distance
        if len(self.station)<=1:
            self.log.info('请先设置单年或者多年分析文件')
            print(r'请先设置',r'请先设置单年或者多年分析文件')
            return None
        #print('self.station',self.station)
        #print('self.start_year',self.start_year)
        #print('self.n_years',self.n_years)
        eq1 = earth.EarthQuake(station= self.station,start_year =self.start_year,n_years=self.n_years)
        print('init_catalog...')
        eq1.init_catalog()
        print('select_catalog_by_distance...')
        self.catalog_distance_pd = eq1.select_catalog_by_distance(self.distance)
        print(r'获取完成',r'获取地震目录数据完成')
        return self.catalog_distance_pd

    def set_yearfile(self):
        txt_file =self.filename
        if len(txt_file) < 3:
            self.txt = ''
        else:
            self.txt = txt_file  # 'F:\\PyVenv\\tkframe\\data\\41001_b_4211_dys_2012-01-01_2012-12-31_126070975.txt'
            path, filename = os.path.split(txt_file)
            name, ext = os.path.splitext(filename)
            print('name:', name)
            ns = name.split('_')
            self.station = ns[0]
            ymd = ns[4].split('-')  # year = int(ns[4])
            year = int(ymd[0])
            print('year:', year)
            self.start_year = year
            self.n_years = 1
            # self.log.info(r"设置单年文件:" + self.txt)

    #设置多年文件
    def set_multfile(self,filename):
        # self.show_frame(MainPage)
        print('call sele.SelePage(self...)')
        self.station = '53079'
        self.start_year = 2006
        self.n_years = 2
        # self.selectPage = sele.SelePage(self.frames[MainPage],self)#(parent,root)
        # self.show_frame(MainPage)

# 原始图绘图函数
    def draw_orig(self,fig):
        fig.clf()
        if self.txt=='':
            print('txt为空')
            return False
        elif  self.tmpdir=='':
            print('路径为空')
            return False
        else:
            ax1 = fig.add_subplot(111)
            plt.ylim(0.0, 10000.0)
            if self.catalog_distance_pd is None:
                self.log.info('请先获取地震目录数据')
                print('无地震目录数据','请先获取地震目录数据')
                return False
                # showerror('无地震目录数据','请先获取地震目录数据')
            else:
                ax2 = ax1.twinx()
                self.draw_earthquake(ax2)
            tozip = stc.Txt2Static(self.txt,self.tmpdir)
            self.pic_filename = tozip.drawLine(ax1,lose=r'NAN')#self.current_file,u'分析图'

# 日线图绘图函数
    def draw_day(self,fig):
        fig.clf()
        if self.txt=='':
            print('错误','单年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            tozip = stc.Txt2Static(self.txt,self.tmpdir)
            self.pic_filename = tozip.drawDateline(ax1,ktype = r'day',lose=r'NAN')#,ktype = r'day'
            #tozip.drawKline(fig,ktype = r'day',lose=r'NAN')#self.current_file,u'分析图'
#月k线图1
    def draw_month_kline(self,fig):
        fig.clf()
        if self.txt=='':
            print('错误','单年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            tozip = stc.Txt2Static(self.txt,self.tmpdir)
            self.pic_filename = tozip.drawKline(ax1,ktype = r'month',lose=r'NAN')#self.current_file,u'分析图'

    # 月线图
    def draw_month(self,fig):
        fig.clf()
        if self.txt=='':
            print('错误','单年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            tozip = stc.Txt2Static(self.txt,self.tmpdir)
            self.pic_filename = tozip.drawDateline(ax1,ktype = r'month',lose=r'NAN')#self.current_file,u'分析图'
    #
    def draw_out(self,fig):
        fig.clf()
        if self.txt=='':
            print('错误','单年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            if self.catalog_distance_pd is None:
                print('无地震目录数据','请先获取地震目录数据')
                return False
            else:
                ax2 = ax1.twinx()
                self.draw_earthquake(ax2)
            tozip = stc.Txt2Static(self.txt,self.tmpdir)
            self.pic_filename = tozip.drawOutlierLine(ax1,lose=r'NAN',out_base=self.out_base)#self.current_file,u'分析图'
    def clear_picture(self,fig):
        fig.clf()

    # ----多年draw------------
    def mult_out_draw(self):
        #self.draw_out(self.figure)
        fig = self.figure
        fig.clf()
        if len(self.txtlist)<1:
            print('错误','多年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            if self.catalog_distance_pd is None:
                print('无地震目录数据','请先获取地震目录数据')
                return False
            else:
                ax2 = ax1.twinx()
                self.draw_earthquake(ax2)
            tozip = lstc.TxtList2Static(self.txtlist,self.tmpdir)
            self.pic_filename = tozip.drawOutlierLine(ax1,lose=r'NAN',out_base=self.out_base)#self.current_file,u'分析图'
        self.show_canvas()
    def mult_month_draw(self):
        #self.draw_month(self.figure)
        fig = self.figure
        fig.clf()
        if len(self.txtlist)<1:
            print('错误','多年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            tozip = lstc.TxtList2Static(self.txtlist,self.tmpdir)
            self.pic_filename = tozip.drawDateline(ax1,ktype = r'month',lose=r'NAN')#self.current_file,u'分析图'
        self.show_canvas()
    def mult_month_draw_kline(self):
        #self.draw_month_kline(self.figure)
        fig = self.figure
        fig.clf()
        if len(self.txtlist)<1:
            print('错误','单年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录没有设置')
            return False
        else:
            ax1 = fig.add_subplot(111)
            tozip = lstc.TxtList2Static(self.txtlist,self.tmpdir)
            self.pic_filename = tozip.drawKline(ax1,ktype = r'month',lose=r'NAN')#self.current_file,u'分析图'
        self.show_canvas()
    def mult_draw(self):
        #self.draw_orig(self.figure)
        fig = self.figure
        fig.clf()
        if len(self.txtlist)<1:
            print('错误','多年分析文件为空')
            return False
        elif  self.tmpdir=='':
            print('错误','临时目录为空')
            return False
        else:
            ax1 = fig.add_subplot(111)
            if self.catalog_distance_pd is None:
                print('无地震目录数据','请先获取地震目录数据')
                return False
            else:
                ax2 = ax1.twinx()
                self.draw_earthquake(ax2)
            tozip = lstc.TxtList2Static(self.txtlist,self.tmpdir)
            self.pic_filename = tozip.drawLine(ax1,lose=r'NAN')#self.current_file,u'分析图'
        self.show_canvas()
    # 地震点
    def draw_earthquake(self,ax):
        ax2 = ax
        ax2.set_ylim(0.0,10.0)
        ax2.set_ylabel('震级o')
        ax2.plot(self.catalog_distance_pd['Ms'],'ro')
        for index,row in  self.catalog_distance_pd.iterrows():
            ax2.axvline(index)
            loc = row[r'mB参考地点'].split('(')#row[r'mB参考地点']
            ax2.annotate('%s'%loc[0],xy=(index,row['Ms']),xytext=(index,row['Ms']+0.5))
            ax2.annotate('%iKM'%row['distance'],xy=(index,row['Ms']),xytext=(index,row['Ms']-0.5))

    def draw(self):
        #canvas = FigureCanvasTkAgg(figure1,winmain)
        #canvas.get_tk_widget().pack(anchor = E , expand=1)
        self.draw_orig(self.figure)
        self.figure.show()
    def day_draw(self):
        self.draw_day(self.figure)
        self.figure.show()

    def month_draw_kline(self):
        self.draw_month_kline(self.figure)
        self.figure.show()
    def show_canvas(self):
        self.figure.show()
    def month_draw(self):
        self.draw_month(self.figure)
        self.figure.show()
    def out_draw(self):
        self.draw_out(self.figure)
        self.figure.show()
    def clear(self):
        self.clear_picture(self.figure)
        self.figure.show()
    def save_pic(self):
        print('self.pic_filename:',self.pic_filename)
        self.figure.savefig(PNG_FILE_NAME)
if __name__ == '__main__':
    # app = Application('data/dongqi/53016_5_4214_dys_2010-01-01_2010-12-31_389782464.txt',500.00,'monthdraw')
    app = Application('/home/xx/workspace/sanictest/data/dongqi/53079_3_4214_dys_2010-01-01_2010-12-31_285600946.txt', 500.0,'daydraw')
    # app.mainloop()
