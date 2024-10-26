import sys

import traceback

import os

from wiki import upload, LogHelper, FileGetter as fg, docTool as dt, JsonTool as jt


# try:
#     from wiki import upload
# except Exception as e:
#     LogHelper.printLog(e)


def getfile(file):
    with open(file, "rb") as f:
        chunk = f.read()

    return chunk


def get_root_dir(dirname):
    ds = dirname.split("\\")
    return dirname if len(ds) <= 1 else ds[0]


# p1 = 'files'
# p2 = 'copyright_files'
# createDir(p1)
# createDir(p2)

hasDescription = False


def letGo(p):
    allfile = fg.readDir(p)
    records = jt.readJsonFile(fg.getData())
    new_all_files = []
    for f in allfile:
        if records.get(f) is None:
            new_all_files.append(f)
            records[f] = {
                "status": "undone",
                "md5": fg.calculate_md5(f)
            }
        else:
            if records[f]["status"] == "undone" or fg.calculate_md5(f) != records[f]["md5"]:
                new_all_files.append(f)
                records[f]["md5"] = fg.calculate_md5(f)
    jt.saveDictAsJson(fg.getData(), records)

    for f in new_all_files:
        stand_file_path = os.path.realpath(f)
        rel_path = os.path.relpath(stand_file_path, p)
        filename = os.path.basename(rel_path)
        filetype = fg.getFileTypeFromPath(filename)
        category = os.path.dirname(rel_path).replace("\\", "_")
        text = ""
        txt = os.path.basename(p) + ".txt"
        if os.path.exists(txt):
            hasDescription = True
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
        # LogHelper.printLog(filetype,filetype not in [".obj", ".mtl"])
        result = upload.prepareUploadWikiWithFile(upload.createPairWithFile(fname, text, chunk))
        if result:
            records[f]["status"] = "done"
            jt.saveDictAsJson(fg.getData(), records)


if __name__ == '__main__':
    root = os.getcwd()
    dirs = [os.path.realpath(os.path.join(root, dir_here)) for dir_here in os.listdir(root) if
            os.path.isdir(dir_here) and not dir_here.startswith(".")]
    # dirs=['test']
    for d in dirs:
        try:
            letGo(d)
        except Exception as e:
            LogHelper.printLog("发生错误：", e)
            # traceback.print_exc()
            LogHelper.printLog(traceback.format_exc(), True)
            pass
    if not hasDescription:
        print("可以创建 文件夹名字.txt 来定义补充文件说明，可以使用的参数有 %filename，%filetype，%category")
    input("按下Enter按钮来退出")
    sys.exit(0)
