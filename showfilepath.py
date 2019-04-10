# showfilePath.py
import os
class showfilepath(object):
    def __init__(self,filename):
        self.filename = filename
    def showfile(self):
        file = []
        for x in self.filename:
            PATH = os.path.dirname(os.path.realpath(__file__))+'/data/'+x
            dirs = os.listdir(PATH)
            for i in dirs:  # 循环读取路径下的文件并筛选输出
                if os.path.splitext(i)[1] == ".zip":  # 筛选csv文件
                    file.append(i)
            return file
if __name__ == '__main__':
    path = showfilepath(['dongqi']).showfile()
    print(path)