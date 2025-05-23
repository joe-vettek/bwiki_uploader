import os.path
import sys
import traceback

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
    input(f"缺少host，可参考格式: https://wiki.biligame.com/xxxx/api.php?")
    sys.exit(0)

if len(host) == 0:
    input(f"缺少host，请在目录下补充，可参考格式: https://wiki.biligame.com/xxxx/api.php?")
    sys.exit(0)

headers = {
    # "Cookie":SESSDATA,
    "User-Agent": "MagicCat Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}

cookie_pass = ""

try:
    cookie_pass = ck.main()
    if len(cookie_pass) == 0:
        raise Exception('Cookie获取错误，如使用固定Cookie信息可以创建名为cookie的文件在目录下，并放入cookie信息')
except Exception as e:
    if os.path.exists('cookie'):
        with open("cookie", "r", encoding="utf-8") as f:
            cookie_pass = f.read()
        if ";" in cookie_pass:
            cookies = cookie_pass.split(";")
            for c in cookies:
                if c.strip().startswith("SESSDATA"):
                    cookie_pass = c.split("=")[-1].strip()
    else:
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
    try:
        res = sessdata.post(host, data=editTittle, headers=headers)
        LogHelper.printLog(jt.strToJson(res.text) + ",")
        return res.json()["edit"]["result"]== "Success"
    except Exception as e:
        traceback.print_exc()
        print(e)
        return False


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
    success = False
    try:
        res = sessdata.post(host, data=editTittle, headers=headers, files={'file': chunk})
        if res.json().get("error") is not None and res.json()["error"]["code"] == "fileexists-no-change":
            success=uploadtoWiki("文件:" + titles, tt, csrftoken)
        else:
            LogHelper.printLog(jt.strToJson(res.text) + ",")
            if res.json().get("upload") is not None and res.json()["upload"].get("result") == "Success":
                success = True
        # 有时候这个文件重复，仅需要更新文字
        if res.json().get("upload") is not None and res.json()["upload"].get("warnings") is not None and \
                res.json()["upload"]["warnings"].get("exists") is not None:
            uploadtoWiki("文件:" + titles, tt, csrftoken)
            success = True

    except Exception as e:
        LogHelper.printLog("文件：{}，长度为{:.2f}MB，错误原因为{}".format(titles, len(chunk) / 1024 ** 2, e), True)

    return success


def prepareUploadWikiWithFileList(allList):
    LogHelper.printLog("[")
    for r in allList:
        prepareUploadWikiWithFile(r)
    LogHelper.printLog("]")


def prepareUploadWikiWithFile(r):
    tokenresponse = sessdata.post(host, headers=headers, data=tokenParams)
    csrftoken = tokenresponse.json()['query']['tokens']['csrftoken']
    LogHelper.printLog("[")
    result = uploadtoWikiWithFile(r["tittle"], r["text"], r["chunk"], csrftoken)
    LogHelper.printLog("]")
    return result
