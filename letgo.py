import traceback

import os
import sys
import wiki.FileGetter as fg
import wiki.docTool as dt

from wiki import upload
# try:
#     from wiki import upload
# except Exception as e:
#     print(e)



def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def getfile(file):
    with open(file, "rb") as f:
        chunk = f.read()

    return chunk


def get_root_dir(dirname):
    ds = dirname.split("\\")
    return dirname if len(ds) <= 1 else ds[0]


p1 = 'files'
p2 = 'copyright_files'
createDir(p1)
createDir(p2)


def letGo(p):
    allfile = fg.readDir(p)
    for f in allfile:
        stand_file_path = os.path.realpath(f)
        rel_path = os.path.relpath(stand_file_path, p)
        filename = os.path.basename(rel_path)
        filetype = fg.getFileTypeFromPath(filename)
        category = os.path.dirname(rel_path).replace("\\", "_")
        text = ""
        txt = os.path.basename(p) + ".txt"
        if os.path.exists(txt):
            try:
                with open(txt) as txtfile:
                    text = txtfile.read() \
                        .replace("%filename", fg.getFileNameFromPath(filename)) \
                        .replace("%filetype", filetype) \
                        .replace("%category", category)
            except:
                with open(txt, encoding="utf-8") as txtfile:
                    text = txtfile.read() \
                        .replace("%filename", fg.getFileNameFromPath(filename)) \
                        .replace("%filetype", filetype) \
                        .replace("%category", category)
        not_special_docx = filetype not in [".obj", ".mtl"]
        chunk = getfile(f) if not_special_docx else dt.get_docx_chunk(f)
        fname = filename if not_special_docx else filename + ".docx"
        # print(filetype,filetype not in [".obj", ".mtl"])
        upload.prepareUploadWikiWithFile([upload.createPairWithFile(fname, text, chunk)])

root = os.getcwd()
dirs = [os.path.realpath(os.path.join(root, dir_here)) for dir_here in os.listdir(root) if
        os.path.isdir(dir_here) and not dir_here.startswith(".")]

for d in dirs:
    try:
        letGo(d)
    except Exception as e:
        print("发生错误：", e)
        traceback.print_exc()
        pass

input("按下任何按钮来退出")
