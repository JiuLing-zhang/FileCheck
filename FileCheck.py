#!/usr/bin/python
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import webbrowser
import pyperclip
import windnd
import hashlib
import os
import time
import base64
from icon import iconBase64

root = Tk()


def GetFileMD5(filePath):
    with open(filePath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash


def GetFileSha1(filePath):
    with open(filePath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash


def SelectFile():
    lblMsg.config(text='')
    filePath = tkinter.filedialog.askopenfilename()
    CalcFileInfo(filePath)


def DraggedFile(files):
    lblMsg.config(text='')
    if len(files) > 1:
        ShowError("只能选择一个文件")
        return
    filePath = files[0].decode("gbk")
    CalcFileInfo(filePath)


def CalcFileInfo(filePath):
    if filePath == "":
        ShowError("请选择文件")
        return

    if md5Var.get() == '0' and sha1Var.get() == '0':
        ShowError("请选择要计算的类型")
        return
    folderPath, fileName = os.path.split(filePath)
    lblFileValue.config(text=fileName)

    fileSize = os.path.getsize(filePath)
    fileSize = int(fileSize/float(1024))
    fileSizeString = format(fileSize, ',')+" KB"
    lblSizeValue.config(text=fileSizeString)

    start_time = int(round(time.time() * 1000))
    md5Value = "-"
    if md5Var.get() == '1':
        md5Value = GetFileMD5(filePath)
    lblMD5Value.config(text=md5Value)

    sha1Value = "-"
    if sha1Var.get() == '1':
        sha1Value = GetFileSha1(filePath)
    lblSha1Value.config(text=sha1Value)

    end_time = int(round(time.time() * 1000))
    millisecond = end_time - start_time
    lblMillisecondValue.config(text="%s ms" % millisecond)
    lblMsg.config(text="点击校验值可复制到剪切板")


def center_window(w, h):
    # 获取屏幕 宽、高
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def CopyMD5Value(event):
    pyperclip.copy(lblMD5Value["text"])
    lblMsg.config(text="md5已复制")


def CopySha1Value(event):
    pyperclip.copy(lblSha1Value["text"])
    lblMsg.config(text="sha1已复制")


def ShowMessage(message):
    tkinter.messagebox.showinfo(title="文件校验工具", message=message)


def ShowError(message):
    tkinter.messagebox.showerror(title="文件校验工具", message=message)


def GotoGitHub(event):
    webbrowser.open("https://github.com/JiuLing-zhang/FileCheck")


if __name__ == "__main__":

    controlRowIndex = 0

    # 校验类型
    md5Var = StringVar(value=0)
    sha1Var = StringVar(value=1)
    lblType = Label(root, text="类型", justify=LEFT)
    lblType.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    chkMd5 = Checkbutton(root, text="md5", variable=md5Var)
    chkMd5.grid(row=controlRowIndex, column=1,  sticky='e')
    chkSha1 = Checkbutton(root, text="Sha1",  variable=sha1Var)
    chkSha1.grid(row=controlRowIndex, column=2, sticky='w')
    controlRowIndex = controlRowIndex + 1

    # 文件名
    lblFile = Label(root, text="文件名", justify=LEFT)
    lblFile.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    lblFileValue = Label(root, text="-", width=52)
    lblFileValue.grid(row=controlRowIndex, column=1, columnspan=2, sticky='w')
    controlRowIndex = controlRowIndex + 1

    # 文件大小
    lblSize = Label(root, text="大小", justify=LEFT)
    lblSize.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    lblSizeValue = Label(root, text="-", justify=LEFT)
    lblSizeValue.grid(row=controlRowIndex, column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # md5
    lblMD5 = Label(root, text="md5", justify=LEFT)
    lblMD5.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    lblMD5Value = Label(root, text="-", justify=LEFT)
    lblMD5Value.bind('<Button-1>', CopyMD5Value)
    lblMD5Value.grid(row=controlRowIndex, column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # Sha1
    lblSha1 = Label(root, text="sha1", justify=LEFT)
    lblSha1.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    lblSha1Value = Label(root, text="-", justify=LEFT)
    lblSha1Value.bind('<Button-1>', CopySha1Value)
    lblSha1Value.grid(row=controlRowIndex, column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # 耗时
    lblMillisecond = Label(root, text="耗时", justify=LEFT)
    lblMillisecond.grid(row=controlRowIndex, column=0, sticky='w', padx=10)
    lblMillisecondValue = Label(root, text="-", justify=LEFT)
    lblMillisecondValue.grid(row=controlRowIndex, column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # 提示
    lblMsg = Label(root, text="请选择文件 或 拖拽文件到窗口", pady=10, justify=LEFT)
    lblMsg.grid(row=controlRowIndex,  column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # 文件选择
    btn = Button(root, text="选择文件", command=SelectFile)
    btn.grid(row=controlRowIndex, column=1, columnspan=2)
    controlRowIndex = controlRowIndex + 1

    # 版本
    lblVersion = Label(root, text="版本 v1.1.0", justify=LEFT)
    lblVersion.grid(row=controlRowIndex, padx=5, column=0)
    # 仓库链接
    githubLink = Label(root, text="GitHub", fg="blue",
                       cursor="hand2", justify=RIGHT)
    githubLink.bind('<Button-1>', GotoGitHub)
    githubLink.grid(row=controlRowIndex, column=2, sticky='e', padx=10)
    controlRowIndex = controlRowIndex + 1

    center_window(440, 240)
    windnd.hook_dropfiles(root, func=DraggedFile)
    root.title("文件校验工具 by 九零")
    root.resizable(height=False, width=False)

    # 解决 pyinstaller 打包时，无法读取图标文件的问题
    # step 1: icon文件转换为 base64格式的 py文件。（通过IcoToBase64Py.py脚本在打包前生成）
    # step 2: 加载 py 文件，并保存为临时的 icon文件。
    # step 3: 读取并设置图标，删除临时文件。
    with open("tmp.ico", mode="w+b") as fi:
        fi.write(base64.b64decode(iconBase64))
    root.iconbitmap("tmp.ico")
    os.remove("tmp.ico")

    root.mainloop()
