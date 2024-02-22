import os
import re
import shutil
import zipfile

from zipfile import ZipFile

import requests


def getFileNameFromPath(path):
    return os.path.splitext(os.path.basename(path))[0]


def readDir(dirPath, filter=None):
    allFiles = []
    __readDir__(dirPath, allFiles)
    return allFiles if filter is None else [i for i in allFiles if i.endswith(filter) or i.endswith(filter.upper())]


def __readDir__(dirPath, allFiles):
    if len(dirPath) == 0:
        print(u'不能为空')
        return
    if dirPath[-1] == '/':
        print(u'文件夹路径末尾不能加/')
        return
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            __readDir__(dirPath + "\\" + f, allFiles)
            # allFiles.append(f)
        return
    else:
        allFiles.append(dirPath)


def is_url(string):
    pattern = r'^https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
    if re.match(pattern, string):
        return True
    else:
        return False


def mycopyfile(srcfile, dstpath):  # 复制函数
    print(srcfile, dstpath)
    if not os.path.exists(srcfile):
        print("%s not exist!" % (srcfile))
        if is_url(srcfile):
            request_download(srcfile, dstpath)
    else:
        # fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        # if not os.path.exists(dstpath):
        #     os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, dstpath)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath))


def request_download(IMAGE_URL, filepath):
    r = requests.get(IMAGE_URL)
    if r.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(r.content)
            print("网络文件，已完成下载")
    else:
        print('网络文件不存在', IMAGE_URL)


def support_gbk(zip_file: ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        try:
            # 注意不一定能cp437
            real_name = name.encode('cp437').decode('gbk')
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        except:
            pass
    return zip_file

def unzip_file(zip_filepath, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with support_gbk(ZipFile(zip_filepath)) as zfp:
        zfp.extractall(dest_path)
