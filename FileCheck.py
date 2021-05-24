#!/usr/bin/python
from tkinter import *
import tkinter.filedialog
import pyperclip
import windnd
import hashlib
import os
root = Tk()


def GetFileMD5(filePath):
    with open(filePath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash


def GetFileSha1(filePath):
    with open(filePath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def SelectFile():
    lblMsg.config(text='')
    filePath = tkinter.filedialog.askopenfilename()
    CalcFileInfo(filePath)


def DraggedFile(files):
    lblMsg.config(text='')
    if len(files) > 1:
        lblMsg.config(text="只能选择一个文件")
        return
    filePath = files[0].decode("gbk")
    CalcFileInfo(filePath)


def CalcFileInfo(filePath):
    if filePath == "":
        lblMsg.config(text="您没有选择任何文件")
        return

    folderPath, fileName = os.path.split(filePath)
    lblFileValue.config(text=fileName)

    fileSize = os.path.getsize(filePath)
    fileSize = int(fileSize/float(1024))
    fileSizeString = format(fileSize, ',')+" KB"
    lblSizeValue.config(text=fileSizeString)

    md5Value = GetFileMD5(filePath)
    lblMD5Value.config(text=md5Value)

    sha1Value = GetFileSha1(filePath)
    lblSha1Value.config(text=sha1Value)

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


if __name__ == "__main__":

    # 文件名
    lblFile = Label(root, text="文件名", justify=LEFT)
    lblFile.grid(row=0, column=0)
    lblFileValue = Label(root, text="-", justify=LEFT)
    lblFileValue.grid(row=0, column=1)

    # 文件大小
    lblSize = Label(root, text="大小", justify=LEFT)
    lblSize.grid(row=1, column=0)
    lblSizeValue = Label(root, text="-", justify=LEFT)
    lblSizeValue.grid(row=1, column=1)

    # md5
    lblMD5 = Label(root, text="md5", justify=LEFT)
    lblMD5.grid(row=2, column=0)
    lblMD5Value = Label(root, text="-", justify=LEFT)
    lblMD5Value.bind('<Button-1>', CopyMD5Value)
    lblMD5Value.grid(row=2, column=1)

    # Sha1
    lblSha1 = Label(root, text="sha1", justify=LEFT)
    lblSha1.grid(row=3, column=0)
    lblSha1Value = Label(root, text="-", justify=LEFT)
    lblSha1Value.bind('<Button-1>', CopySha1Value)
    lblSha1Value.grid(row=3, column=1)

    # 提示
    lblMsg = Label(root, text="请选择文件 或 拖拽文件到窗口", justify=LEFT)
    lblMsg.grid(row=4, column=1)

    # 文件选择
    btn = Button(root, text="选择文件", command=SelectFile)
    btn.grid(row=5, column=1)

    center_window(350, 160)
    windnd.hook_dropfiles(root, func=DraggedFile)
    root.title("文件校验工具 by 九零")
    root.mainloop()
