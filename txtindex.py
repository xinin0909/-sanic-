# txt2index.py
import numpy as np
import os, json
import os.path

import logger  # 日志模块


# 为txt文件建立dict(or json)索引
class Txt2index(object):
    def __init__(self, datadir='', indexdict={}):
        self.log = logger.logger
        self.datadir = datadir
        print(datadir)
        if (not indexdict) or (indexdict is None):  # not
            self.indexdict = {}
            self.station = set([])
            self.type = set([])
            self.device = set([])
            self.starttime = set([])
            print('indexdict(empty):', indexdict)
        else:
            self.indexdict = indexdict
            self.station = set(indexdict['station'])
            self.type = set(indexdict['type'])
            self.device = set(indexdict['device'])
            self.starttime = set(indexdict['starttime'])
            print('indexdict data:', indexdict)
        print(self.indexdict)
        if not self.datadir or len(self.datadir) <= 2:
            self.datadir = os.getcwd() + os.path.sep + 'data'
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def txt2indexOld(self):
        for parent, dirnames, filenames in os.walk(self.datadir):
            for filename in filenames:
                txt = os.path.join(parent, filename)
                name, ext = os.path.splitext(filename)
                ns = name.split('_')
                # print(ns)
                # filedict={'origin':[{ns[0]:[{ns[2]:[{ns[1]:[{ns[3]:{'date':[ns[4],ns[5]],'filename':txt} } ]}]} ]}] }
                keyname = 'origin_' + ns[0] + '_' + ns[2] + '_' + ns[1] + '_' + ns[4]
                filedict = {keyname: {'datetype': ns[3], 'date': [ns[4], ns[5]], 'filename': txt}}
                # print(filedict)
                # indexdict = self.indexdict
                # indexdict.update(filedict)
                # self.indexdict = indexdict
                self.indexdict.update(filedict)
                self.station.add(ns[0])
                self.type.add(ns[2])
                self.device.add(ns[1])
                self.starttime.add(ns[4])

                # print(self.indexdict)
                # self.indexdict = dict(self.indexdict, **filedict)
                # self.indexdict = dict(self.indexdict.items()+filedict.items())
                # print(self.indexdict)
        print('---------------')
        print({'station': list(self.station)})
        print({'type': list(self.type)})
        print({'device': list(self.device)})
        print({'starttime': list(self.starttime)})
        self.indexdict.update({'station': list(self.station)})
        self.indexdict.update({'type': list(self.type)})
        self.indexdict.update({'device': list(self.device)})
        self.indexdict.update({'starttime': list(self.starttime)})
        keyitem = 'origin_' + self.indexdict['station'][0] + '_' + self.indexdict['type'][0] + '_' + \
                  self.indexdict['device'][0] + '_' + self.indexdict['starttime'][0]
        print('first key:', keyitem)
        print('is in:', keyitem in self.indexdict.keys())
        # self.indexdict
        # print(self.indexdict)
        print('---------------')
        # json.dumps(self.indexdict)
        # print(json.dumps(self.indexdict))

        return self.indexdict

    def txt2index(self):
        print(self.datadir)
        file_list = os.listdir(self.datadir)
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.txt':
                self.log.info(file_name)
                txt = os.path.join(self.datadir, file_name)
                name, ext = os.path.splitext(file_name)
                ns = name.split('_')
                # print(ns)
                # filedict={'origin':[{ns[0]:[{ns[2]:[{ns[1]:[{ns[3]:{'date':[ns[4],ns[5]],'filename':txt} } ]}]} ]}] }
                keyname = 'origin_' + ns[0] + '_' + ns[2] + '_' + ns[1] + '_' + ns[4]
                filedict = {keyname: {'datetype': ns[3], 'date': [ns[4], ns[5]], 'filename': txt}}
                # print(filedict)
                '''indexdict = self.indexdict
                indexdict.update(filedict)
                self.indexdict = indexdict'''
                self.indexdict.update(filedict)
                self.station.add(ns[0])
                self.type.add(ns[2])
                self.device.add(ns[1])
                self.starttime.add(ns[4])
        print('---------------')
        print({'station': list(self.station)})
        print({'type': list(self.type)})
        print({'device': list(self.device)})
        print({'starttime': list(self.starttime)})
        self.indexdict.update({'station': list(self.station)})
        self.indexdict.update({'type': list(self.type)})
        self.indexdict.update({'device': list(self.device)})
        self.indexdict.update({'starttime': list(self.starttime)})
        keyitem = 'origin_' + self.indexdict['station'][0] + '_' + self.indexdict['type'][0] + '_' + \
                  self.indexdict['device'][0] + '_' + self.indexdict['starttime'][0]
        print('first key:', keyitem)
        print('is in:', keyitem in self.indexdict.keys())
        # self.indexdict
        # print(self.indexdict)
        print('---------------')
        # json.dumps(self.indexdict)
        # print(json.dumps(self.indexdict))

        return self.indexdict


# usage:
if __name__ == "__main__":
    print('--------txt2index-------')
    t2i = Txt2index(datadir='data/yichuqidon')
    indexdict = t2i.txt2index()
    print(json.dumps(indexdict))
    print(indexdict['starttime'])
    print('---------------')

