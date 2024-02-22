import os
import sys
import wiki.FileGetter as fg
import wiki.docTool as dt

# from wiki import upload
try:
    from wiki import upload
except Exception as e:
    print(e)
    input("请在微软Edge浏览器上登录b站账号，并关闭浏览器（可以在cmd中输入‘taskkill /F /IM msedge.exe’）")
    sys.exit(0)


def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def getfile(file):
    with open(file, "rb") as f:
        chunk = f.read()

    return chunk


p1 = 'files'
p2 = 'copyright_files'
createDir(p1)
createDir(p2)


def letGo(p, needCopyRight):
    for d in os.listdir(p):
        path = os.path.join(p, d)
        if os.path.isdir(path):
            for f in os.listdir(path):
                filepath = os.path.join(path, f)
                filetype = fg.getFileTypeFromPath(f)
                text = "== 许可协议 ==\n{{Copyright}}\n\n" if needCopyRight else ""
                text += "[[Category:{}]]".format(d)
                not_special_docx = filetype not in [".obj", ".mtl"]
                chunk = getfile(filepath) if not_special_docx else dt.get_docx_chunk(filepath)
                fname = f if not_special_docx else f + ".docx"
                # print(filetype,filetype not in [".obj", ".mtl"])
                upload.prepareUploadWikiWithFile([upload.createPairWithFile(fname, text, chunk)])


letGo(p1, False)
letGo(p2, True)

input("按下任何按钮来退出")
