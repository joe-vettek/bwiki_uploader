import os
import threading
import time


from wiki import FileGetter as fg
import datetime
import tkinter as tk


output = None


def standardPath(pathText):
    result = ""
    if type(pathText) == list:
        for i in pathText:
            result += str(i) + "，"
        result = result[:-1]
    else:
        result = str(pathText)

    return result.strip().replace("//", "\\").replace("/", "\\").replace("'", "")


def addToOutPut(textInfo, isError=False):
    if not output is None:
        output.config(state='normal')
        output.insert("end", textInfo)
        # 强制移动到最新
        output.see(tk.constants.END)
        output.update()
        output.config(state='disabled')
        if isError:
            linesCount = float(output.index('end'))
            # print(str(linesCount-len(textInfo.split("\n"))), str(linesCount))
            output.tag_add("error", str(linesCount - len(textInfo.split("\n"))), str(linesCount - 1.0))


def betterNum(num):
    return ("0" + str(num) if int(num) < 10 else num)


logNow = None
logCount=0

def printLog(logInfo, isError=False):
    global logCount
    logCount+=1
    # 避免过度消耗内存
    if logCount>120:
        if not output is None:
            output.config(state='normal')
            output.delete(1.0, 2.0)
            output.update()
            output.config(state='disabled')

    logInfo = str(logInfo)
    print(logInfo)
    addToOutPut(logInfo + '\n', isError)
    i = datetime.datetime.now()
    with open(logNow, "a", encoding="utf-8") as f:
        logInfo = '[{}年{}月{}日 {}:{}:{}] '.format(i.year, betterNum(i.month), betterNum(i.day), betterNum(i.hour),
                                                betterNum(i.minute), betterNum(i.second)) + logInfo + '\n'
        f.write(logInfo)
        f.close()


def printNew():
    i = datetime.datetime.now()
    times = 0
    global logNow
    logNow = fg.join(fg.getLogDir(), "{}-{}-{}.log".format(i.year, betterNum(i.month), betterNum(i.day)))
    while os.path.exists(logNow):
        times += 1
        logNow = fg.join(fg.getLogDir(), "{}-{}-{}-{}.log".format(i.year, betterNum(i.month), betterNum(i.day), times))


printNew()