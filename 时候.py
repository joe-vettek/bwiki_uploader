from os.path import join

import os

from wiki import LogHelper
from wiki.FileGetter import readDir,getFileNameFromPath,getFileTypeFromPath

pa = r'C:\Users\Admin\Desktop\卡拉彼丘MMD导出 - 副本'

files = readDir(pa, 'mtl')
files.extend(readDir(pa, 'obj'))

all=[]
for f in files:
    basef=os.path.basename(f)
    n=getFileNameFromPath(basef).split("-模型")[0]
    if n not in all:
        all.append(n)
    # if '模型' not in basef:
    #     t=getFileTypeFromPath(basef)
    #     name=getFileNameFromPath(basef)
    #     dir=os.path.dirname(f)
    #     os.rename(f,join(dir,"{}-模型{}".format(name,t)))
    #     LogHelper.printLog(join(dir,"{}-模型{}".format(name,t)))
# LogHelper.printLog(files)
LogHelper.printLog(";\n".join(all))