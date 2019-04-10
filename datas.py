import numpy as np
import os, json
import os.path
import zipfile

# from zfile import ZFile
# import logger  # 日志


# 解压缩.zip文件为txt文件
class Txtzip2txt(object):
    def __init__(self, basedir='', todir=''):  # ,indexdict={}
        # self.log = logger.logger
        self.fullnamefiles = []  # np.array(0)
        self.files = []
        self.basedir = basedir
        self.todir = todir
        '''if (not indexdict) or (indexdict is not None): 
            self.indexdict = {}
            self.station = set([])
            self.type =  set([])
            self.device =  set([])
            self.starttime =  set([])
        else:
            self.indexdict = indexdict
            self.station = set(indexdict['station'])
            self.type = set(indexdict['type'])
            self.device = set(indexdict['device'])
            self.starttime =  set(indexdict['starttime'])
        print(self.indexdict)'''
        print(self.todir)
        if not self.basedir or len(self.basedir) < 3:
            self.basedir = os.getcwd()  # os.path.dirname(self)
        if not self.todir or len(self.todir) < 3:
            self.todir = os.getcwd() + os.path.sep + 'data'
        if not os.path.exists(self.basedir):
            # self.log.error('zip文件目录' + self.basedir + '不存在！')
            print('不存在')
            # os.makedirs(self.basedir)
        if not os.path.exists(self.todir):
            os.makedirs(self.todir)
        '''for parent,dirnames,filenames in os.walk(self.basedir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            #for dirname in  dirnames:  #文件夹信息
                #print(parent+":"+dirname)
            for filename in filenames:
                #print (parent+":" + filename)     #输出文件路径信息
                name,ext = os.path.splitext(filename)                
                if ext == '.zip':
                    self.fullnamefiles.append(""+os.path.join(parent,filename))
                    self.files.append(""+filename)
                    self.log.info('zip文件:'+filename)
                else:
                    self.log.error('不是zip文件，文件名:'+filename)
                    #print(ext)

    def txtzip2txt(self):
        for fullname in self.fullnamefiles:
            try:
                txtz = ZFile(fullname)   
                txtz.extract_to(self.todir) #txtdir  
                txtz.close()
            except:
                return False
        print(self.todir)
        return True'''

    def txtzip2txt(self):  # zipExtract
        file_list = os.listdir(self.basedir)
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.zip':
                # self.log.info(file_name)
                file_fullname = os.path.join(self.basedir, file_name)
                file_zip = zipfile.ZipFile(file_fullname, 'r')
                for file in file_zip.namelist():
                    file_zip.extract(file, self.todir)
                file_zip.close()
        return True

    def txt2indexOld(self):
        for parent, dirnames, filenames in os.walk(self.todir):
            for filename in filenames:
                txt = os.path.join(parent, filename)
                name, ext = os.path.splitext(filename)
                ns = name.split('_')
                # print(ns)
                # filedict={'origin':[{ns[0]:[{ns[2]:[{ns[1]:[{ns[3]:{'date':[ns[4],ns[5]],'filename':txt} } ]}]} ]}] }
                keyname = 'origin_' + ns[0] + '_' + ns[2] + '_' + ns[1] + '_' + ns[4]
                filedict = {keyname: {'datetype': ns[3], 'date': [ns[4], ns[5]], 'filename': txt}}
                # print(filedict)
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
        print(keyitem)
        # self.indexdict
        # print(self.indexdict)
        print('---------------')
        # json.dumps(self.indexdict)
        # print(json.dumps(self.indexdict))

        return self.indexdict


# 为txt文件建立dict(or json)索引
class Txt2index(object):
    def __init__(self, datadir='', indexdict={}):
        # self.log = logger.logger
        self.datadir = datadir
        if (not indexdict) or (indexdict is not None):
            self.indexdict = {}
            self.station = set([])
            self.type = set([])
            self.device = set([])
            self.starttime = set([])
        else:
            self.indexdict = indexdict
            self.station = set(indexdict['station'])
            self.type = set(indexdict['type'])
            self.device = set(indexdict['device'])
            self.starttime = set(indexdict['starttime'])
        print(self.indexdict)
        if not self.datadir or len(self.datadir) < 3:
            self.datadir = os.getcwd() + os.path.sep + 'data/dongqi'
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
        print(keyitem)
        print(keyitem in self.indexdict.keys())
        # self.indexdict
        # print(self.indexdict)
        print('---------------')
        # json.dumps(self.indexdict)
        # print(json.dumps(self.indexdict))

        return self.indexdict

    def txt2index(self):
        file_list = os.listdir(self.datadir)
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.txt':
                # self.log.info(file_name)
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
        print(keyitem)
        print(keyitem in self.indexdict.keys())
        # self.indexdict
        # print(self.indexdict)
        print('---------------')
        # json.dumps(self.indexdict)
        # print(json.dumps(self.indexdict))

        return self.indexdict


# usage:
if __name__ == "__main__":
    # a = Txtzip2txt('F:\\PyVenv\\data')
    a = Txtzip2txt('data/dongqi')
    # for fullname in a.fullnamefiles:
    # print(fullname)
    a.txtzip2txt()
    # a.zipExtract()
    print('--------txt2index-------')
    b = Txt2index()
    indexdict = b.txt2index()
    print(json.dumps(indexdict))
    print('---------------')
    # for name in a.files:
    #    print(name)
