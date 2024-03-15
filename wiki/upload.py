import os.path
import sys

from requests import Session

from wiki import LogHelper, GetCookie as ck, JsonTool as jt

host = ""
if os.path.exists("host"):
    with open("host", "r", encoding="utf-8") as f:
        host = f.read()
        LogHelper.printLog(f"Host: {host}")
else:
    with open("host", "w", encoding="utf-8") as f:
        pass
    input(f"缺少host，可参考格式: https://wiki.biligame.com/wikia/api.php?")
    sys.exit(0)

if len(host) == 0:
    input(f"缺少host，请在目录下补充，可参考格式: https://wiki.biligame.com/wikia/api.php?")
    sys.exit(0)

headers = {
    # "Cookie":SESSDATA,
    "User-Agent": "MagicCat Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}

cookie_pass = ""

try:
    cookie_pass = ck.main()
except Exception as e:
    LogHelper.printLog(e)
    input("请在微软Edge浏览器上登录b站账号，并关闭浏览器（可以在cmd中输入‘taskkill /F /IM msedge.exe’）")
    sys.exit(0)

sessdata = Session()

sessdata.cookies.update({"SESSDATA": cookie_pass})

tokenParams = {
    'action': 'query',
    'format': 'json',
    'meta': 'tokens',
}


# csrftoken=""

def uploadtoWiki(titles, tt, csrftoken):
    # if csrftoken=="":
    #     tokenresponse = requests.post(host, headers=headers, data=tokenParams)
    #     csrftoken=tokenresponse.json()['query']['tokens']['csrftoken']
    # # 进行编辑
    editTittle = {
        'action': 'edit', 'title': titles, 'format': 'json',
        'summary': '自动化编辑', 'text': tt,
        'token': csrftoken
    }
    #
    res = sessdata.post(host, data=editTittle, headers=headers)
    LogHelper.printLog(jt.strToJson(res.text) + ",")


def prepareUploadWiki(allList):
    tokenresponse = sessdata.post(host, headers=headers, data=tokenParams)
    csrftoken = tokenresponse.json()['query']['tokens']['csrftoken']
    LogHelper.printLog("[")
    for r in allList:
        uploadtoWiki(r["tittle"], r["text"], csrftoken)
    LogHelper.printLog("]")


def createPair(tittle, text):
    return {"tittle": tittle, "text": text}


def createPairWithFile(tittle, text, chunk):
    return {"tittle": tittle, "text": text, "chunk": chunk}


def uploadtoWikiWithFile(titles, tt, chunk, csrftoken):
    editTittle = {
        'action': 'upload', 'filename': titles, 'format': 'json',
        'comment': '自动化编辑', 'text': tt,
        'token': csrftoken, "ignorewarnings": True
    }
    res = sessdata.post(host, data=editTittle, headers=headers, files={'file': chunk})
    try:
        if res.json().get("error") is not None and res.json()["error"]["code"] == "fileexists-no-change":
            uploadtoWiki("文件:" + titles, tt, csrftoken)
        else:
            LogHelper.printLog(jt.strToJson(res.text) + ",")
        # 有时候这个文件重复，仅需要更新文字
        if res.json().get("upload") is not None and res.json()["upload"].get("warnings") is not None and \
                res.json()["upload"]["warnings"].get("exists") is not None:
            uploadtoWiki("文件:" + titles, tt, csrftoken)
    except Exception as e:
        LogHelper.printLog("文件{}长度为{:.2f}MB".format(titles, len(chunk) / 1024 ** 2), e)


def prepareUploadWikiWithFile(allList):
    tokenresponse = sessdata.post(host, headers=headers, data=tokenParams)
    csrftoken = tokenresponse.json()['query']['tokens']['csrftoken']
    LogHelper.printLog("[")
    for r in allList:
        uploadtoWikiWithFile(r["tittle"], r["text"], r["chunk"], csrftoken)
    LogHelper.printLog("]")
