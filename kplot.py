# 画K线图的函数
# 输入的开高低收都是ndarray格式的一个向量
import time
import sys
import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
import pandas as pd


#
def KplotByAx(ax, pic_name, Mean, Max, Min, Median):
    length = len(Median)
    nan = np.nan
    # fig = plt.figure()
    ax1 = ax
    # ax1 = plt.axes()#[0,0,3,2]

    X = np.array(range(0, length))
    pad_nan = X + nan

    # 计算上 下影线
    max_clop = Median.copy()
    max_clop[Median < Mean] = Mean[Median < Mean]
    min_clop = Median.copy()
    min_clop[Median > Mean] = Mean[Median > Mean]

    # 上影线
    line_up = np.array([Max, max_clop, pad_nan])
    line_up = np.ravel(line_up, 'F')
    # 下影线
    line_down = np.array([Min, min_clop, pad_nan])
    line_down = np.ravel(line_down, 'F')

    # 计算上下影线对应的X坐标
    pad_nan = nan + X
    pad_X = np.array([X, X, X])
    pad_X = np.ravel(pad_X, 'F')

    # 画出实体部分,先画收盘价在上的部分
    up_cl = Median.copy()
    up_cl[Median <= Mean] = nan
    up_op = Mean.copy()
    up_op[Median <= Mean] = nan

    down_cl = Median.copy()
    down_cl[Mean <= Median] = nan
    down_op = Mean.copy()
    down_op[Mean <= Median] = nan

    even = Median.copy()
    even[Median != Mean] = nan

    # 画出收红的实体部分
    pad_box_up = np.array([up_op, up_op, up_cl, up_cl, pad_nan])
    pad_box_up = np.ravel(pad_box_up, 'F')
    pad_box_down = np.array([down_cl, down_cl, down_op, down_op, pad_nan])
    pad_box_down = np.ravel(pad_box_down, 'F')
    pad_box_even = np.array([even, even, even, even, pad_nan])
    pad_box_even = np.ravel(pad_box_even, 'F')

    # X的nan可以不用与y一一对应
    X_left = X - 0.25
    X_right = X + 0.25
    box_X = np.array([X_left, X_right, X_right, X_left, pad_nan])
    box_X = np.ravel(box_X, 'F')

    # Median_handle=plt.plot(pad_X,line_up,color='k')

    vertices_up = np.array([box_X, pad_box_up]).T
    vertices_down = np.array([box_X, pad_box_down]).T
    vertices_even = np.array([box_X, pad_box_even]).T

    handle_box_up = mat.patches.Polygon(vertices_up, color='r', zorder=1, label='Median>Mean')
    handle_box_down = mat.patches.Polygon(vertices_down, color='g', zorder=1, label='Median<Mean')  # ,label='Median'
    handle_box_even = mat.patches.Polygon(vertices_even, color='k', zorder=1)  # ,label='Mean'
    # matplotlib.patches
    ax1.add_patch(handle_box_up)
    ax1.add_patch(handle_box_down)
    ax1.add_patch(handle_box_even)

    handle_line_up = mat.lines.Line2D(pad_X, line_up, color='b', linestyle='solid', zorder=0, label='Max')
    handle_line_down = mat.lines.Line2D(pad_X, line_down, color='k', linestyle='solid', zorder=0, label='Min')

    ax1.add_line(handle_line_up)
    ax1.add_line(handle_line_down)

    v = [0, length, Mean.min() - 0.5, Mean.max() + 0.5]

    ax1.axis(v)
    ax1.set_title(pic_name)
    ax1.legend()
    # plt.axis(v)
    # plt.legend()
    # plt.show()


#
def KplotByFig(fig, pic_name, Mean, Max, Min, Median):
    length = len(Median)
    nan = np.nan
    # fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax1 = plt.axes()#[0,0,3,2]

    X = np.array(range(0, length))
    pad_nan = X + nan

    # 计算上 下影线
    max_clop = Median.copy()
    max_clop[Median < Mean] = Mean[Median < Mean]
    min_clop = Median.copy()
    min_clop[Median > Mean] = Mean[Median > Mean]

    # 上影线
    line_up = np.array([Max, max_clop, pad_nan])
    line_up = np.ravel(line_up, 'F')
    # 下影线
    line_down = np.array([Min, min_clop, pad_nan])
    line_down = np.ravel(line_down, 'F')

    # 计算上下影线对应的X坐标
    pad_nan = nan + X
    pad_X = np.array([X, X, X])
    pad_X = np.ravel(pad_X, 'F')

    # 画出实体部分,先画收盘价在上的部分
    up_cl = Median.copy()
    up_cl[Median <= Mean] = nan
    up_op = Mean.copy()
    up_op[Median <= Mean] = nan

    down_cl = Median.copy()
    down_cl[Mean <= Median] = nan
    down_op = Mean.copy()
    down_op[Mean <= Median] = nan

    even = Median.copy()
    even[Median != Mean] = nan

    # 画出收红的实体部分
    pad_box_up = np.array([up_op, up_op, up_cl, up_cl, pad_nan])
    pad_box_up = np.ravel(pad_box_up, 'F')
    pad_box_down = np.array([down_cl, down_cl, down_op, down_op, pad_nan])
    pad_box_down = np.ravel(pad_box_down, 'F')
    pad_box_even = np.array([even, even, even, even, pad_nan])
    pad_box_even = np.ravel(pad_box_even, 'F')

    # X的nan可以不用与y一一对应
    X_left = X - 0.25
    X_right = X + 0.25
    box_X = np.array([X_left, X_right, X_right, X_left, pad_nan])
    box_X = np.ravel(box_X, 'F')

    # Median_handle=plt.plot(pad_X,line_up,color='k')

    vertices_up = np.array([box_X, pad_box_up]).T
    vertices_down = np.array([box_X, pad_box_down]).T
    vertices_even = np.array([box_X, pad_box_even]).T

    handle_box_up = mat.patches.Polygon(vertices_up, color='r', zorder=1, label='Median>Mean')
    handle_box_down = mat.patches.Polygon(vertices_down, color='g', zorder=1, label='Median<Mean')  # ,label='Median'
    handle_box_even = mat.patches.Polygon(vertices_even, color='k', zorder=1)  # ,label='Mean'
    # matplotlib.patches
    ax1.add_patch(handle_box_up)
    ax1.add_patch(handle_box_down)
    ax1.add_patch(handle_box_even)

    handle_line_up = mat.lines.Line2D(pad_X, line_up, color='b', linestyle='solid', zorder=0, label='Max')
    handle_line_down = mat.lines.Line2D(pad_X, line_down, color='k', linestyle='solid', zorder=0, label='Min')

    ax1.add_line(handle_line_up)
    ax1.add_line(handle_line_down)

    v = [0, length, Mean.min() - 0.5, Mean.max() + 0.5]

    ax1.axis(v)
    ax1.set_title(pic_name)
    ax1.legend()
    # plt.axis(v)
    # plt.legend()
    # plt.show()


# ------------------------------------
def Kplot(Mean, Max, Min, Median):
    length = len(Median)
    nan = np.nan
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax1 = plt.axes()#[0,0,3,2]

    X = np.array(range(0, length))
    pad_nan = X + nan

    # 计算上 下影线
    max_clop = Median.copy()
    max_clop[Median < Mean] = Mean[Median < Mean]
    min_clop = Median.copy()
    min_clop[Median > Mean] = Mean[Median > Mean]

    # 上影线
    line_up = np.array([Max, max_clop, pad_nan])
    line_up = np.ravel(line_up, 'F')
    # 下影线
    line_down = np.array([Min, min_clop, pad_nan])
    line_down = np.ravel(line_down, 'F')

    # 计算上下影线对应的X坐标
    pad_nan = nan + X
    pad_X = np.array([X, X, X])
    pad_X = np.ravel(pad_X, 'F')

    # 画出实体部分,先画收盘价在上的部分
    up_cl = Median.copy()
    up_cl[Median <= Mean] = nan
    up_op = Mean.copy()
    up_op[Median <= Mean] = nan

    down_cl = Median.copy()
    down_cl[Mean <= Median] = nan
    down_op = Mean.copy()
    down_op[Mean <= Median] = nan

    even = Median.copy()
    even[Median != Mean] = nan

    # 画出收红的实体部分
    pad_box_up = np.array([up_op, up_op, up_cl, up_cl, pad_nan])
    pad_box_up = np.ravel(pad_box_up, 'F')
    pad_box_down = np.array([down_cl, down_cl, down_op, down_op, pad_nan])
    pad_box_down = np.ravel(pad_box_down, 'F')
    pad_box_even = np.array([even, even, even, even, pad_nan])
    pad_box_even = np.ravel(pad_box_even, 'F')

    # X的nan可以不用与y一一对应
    X_left = X - 0.25
    X_right = X + 0.25
    box_X = np.array([X_left, X_right, X_right, X_left, pad_nan])
    box_X = np.ravel(box_X, 'F')

    # Median_handle=plt.plot(pad_X,line_up,color='k')

    vertices_up = np.array([box_X, pad_box_up]).T
    vertices_down = np.array([box_X, pad_box_down]).T
    vertices_even = np.array([box_X, pad_box_even]).T

    handle_box_up = mat.patches.Polygon(vertices_up, color='r', zorder=1, label='Median&Mean')
    handle_box_down = mat.patches.Polygon(vertices_down, color='g', zorder=1)  # ,label='Median'
    handle_box_even = mat.patches.Polygon(vertices_even, color='k', zorder=1)  # ,label='Mean'
    # matplotlib.patches
    ax1.add_patch(handle_box_up)
    ax1.add_patch(handle_box_down)
    ax1.add_patch(handle_box_even)

    handle_line_up = mat.lines.Line2D(pad_X, line_up, color='b', linestyle='solid', zorder=0, label='Max')
    handle_line_down = mat.lines.Line2D(pad_X, line_down, color='k', linestyle='solid', zorder=0, label='Min')

    ax1.add_line(handle_line_up)
    ax1.add_line(handle_line_down)

    v = [0, length, Mean.min() - 0.5, Mean.max() + 0.5]

    ax1.axis(v)
    ax1.set_title(u'kline')
    ax1.legend()
    # plt.axis(v)
    # plt.legend()
    plt.show()


'''
STOCK = '600704'
df2 = pd.read_csv("stock/ok%s.csv"%STOCK, index_col='date')
df2.index = pd.to_datetime(df2.index)
df = df2.sort_index()
Kplot(df[u'Mean'],df[u'Max'],df[u'Min'],df[u'Median'])
#'''
'''
import time
import sys

import matplotlib.pyplot as plt
import matplotlib as mat

import numpy as np

code='000001.XSHG'

start_date='2005-11-01'
end_date='2016-1-28'
Stock_data=get_price(code, start_date=start_date, end_date=end_date, frequency='daily',fields= ['Mean',  'Max', 'Min','Median', 'volume', 'money'])

Stock_data2=Stock_data.values
Median=Stock_data2[:,3]

#删掉所有的nan行，但其实删不删问题都不大
Stock_data2=Stock_data2[~np.isnan(Median),:]


Median=Stock_data2[:,3]
Mean=Stock_data2[:,0]
Max=Stock_data2[:,1]
Min=Stock_data2[:,2]

%time Kplot(Mean,Max,Min,Median)
CPU times: user 65.7 ms, sys: 561 µs, total: 66.2 ms
Wall time: 66.7 ms

'''
