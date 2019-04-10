# Zfile.py
import zipfile
import os.path
import os
import sys
import io

# sys.path.append(r'F:\\TimeSrs')
# from allfiles import AllFiles


class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)
        print('__init__:' + self.basedir + ',' + filename)

    '''def addfile(self, path, arcname=None):   
        path = path.replace('//', '/')
        if not arcname:   
            if path.startswith(self.basedir):   
                arcname = path[len(self.basedir):]   
            else:   
                arcname = ''
        print('addfile:'+arcname) #+path+','
        self.zfile.write(path, arcname) 
    def addfiles(self, paths):   
        for path in paths:            
            if isinstance(path, tuple):   
                self.addfile(*path)   
            else:   
                self.addfile(path)
    #假设要把一个叫path中的文件全部添加到压缩包里（这里只添加一级子目录中的文件）
    def addfile_bak(self, path):
        sourceFiles = os.listdir(path)
        if sourceFiles == None or len(sourceFiles) < 1:
            print (">>>>>> 待压缩的文件目录：" + path + " 里面不存在文件,无需压缩. <<<<<<")
        else:
            #zipFileFullDir = os.path.join(zipFilePath, fileName)
            #z = zipfile.ZipFile(zipFileFullDir, 'w' ,zipfile.ZIP_DEFLATED)
            for sourceFile in sourceFiles:
                sourceFileFullDir = os.path.join(sourceFilePath, sourceFile)
                # sourceFileFullDir是文件的全路径，sourceFile是文件名，这样就能达到你要的目的了
                self.zfile.write(sourceFileFullDir, sourceFile)
                print(sourceFileFullDir+','+ sourceFile)'''

    # 假设要把一个叫path中的文件全部添加到压缩包里（这里只添加一级子目录中的文件）
    def addfile(self, path):  # , arcname=None _with_path
        # print(path)
        if os.path.isdir(path):
            for d in os.listdir(path):
                print(path + os.sep + d)
                self.zfile.write(path + os.sep + d, d)  # 压缩参数1并改名为参数2
                # close() 是必须调用的！
                # z.close()
        else:
            print(">>>>>> 待压缩的文件目录：" + path + " 里面不存在,无需压缩. <<<<<<")

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            # print('extract_to:'+path+','+p)
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            print('extract:' + f)
            open(f, 'wb').write(self.zfile.read(filename))
            # self.zfile(f, 'wb').write(self.zfile.read(filename))


def create(zfile, files):
    z = ZFile(zfile, 'w')
    z.addfile(files)
    z.close()


def extract(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()
# files = AllFiles("F:\\TimeSrs\\aa")
# create("F:\\TimeSrs\\aa.zip",files.fullnamefiles)#\台站.xls
# extract("F:\\TimeSrs\\aa.zip", "F:\\TimeSrs\\aa\\ee")
