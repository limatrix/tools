import hashlib
import sys
import os
import shutil
from tkinter import *
from tkinter.filedialog import askdirectory

global globalEntry
global globalButton
global globalText
global pathlst

global_list = []
global_repeated = ''
global_delete = False

pathlst = []

def calc_md5(fname):
    md5 = hashlib.md5()
    with open(fname, 'rb') as fp:
        print('checking %s' % fname)
        while True:
            block = fp.read(8192)
            if not block:
                break
            else:
                md5.update(block)
        md5hex = md5.hexdigest()
        fp.close()
    return md5hex

def repeated_opts(f, fname):
    global global_delete
    global global_repeated
    global globalText

    if global_delete is False:
        count = 1
        target_name = os.path.join(global_repeated, f)
        while os.path.exists(target_name):
            (name, ext) = os.path.splitext(f)
            ends = '_%d' % count
            count = count + 1
            if name.endswith(ends):
                f = '%s%d%s' % (name[0:-1], count, ext)
            else:
                f = '%s_%d%s' % (name, count, ext)
            target_name = os.path.join(global_repeated, f)
        else:
            print('move %s to %s as %s' % (fname, global_repeated, f))
            shutil.move(fname, target_name)
    else:
        globalText.insert(END, ('delete %s' % fname))
        os.remove(fname)

def find_repeated(directory):
    global global_list
    for root, dirs, files in os.walk(directory):
        for f in files:
            fname = os.path.join(root, f)
            md5hex = calc_md5(fname)
            if md5hex not in global_list:
                global_list.append(md5hex)
            else:
                repeated_opts(f, fname)
            pass
        pass
    pass

def selectPath(p):
	global pathlst
	_path = askdirectory()
	pathlst[p].set(_path)

def targetDialogOpt(opt):
	global globalEntry, globalButton, global_delete

	if opt == 2:
		globalEntry.grid(row = 0, column = 3)
		globalButton.grid(row = 0, column = 4, padx = 7)
	elif opt == 1:
		globalEntry.grid_remove() 
		globalButton.grid_remove()
		global_delete = True

def findRepeated():
	global globalText, pathlst, global_repeated, global_delete
	global_repeated = pathlst[4].get()
	for i in range(4):
		path = pathlst[i].get()
		if path:
			find_repeated(path)
		pass
	pass

root = Tk()
root.title("重复文件管理")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)
for i in range(5):
	pathlst.append(StringVar())

radioVar = IntVar()
# top frame
topFrame = Frame(root, height = 200, width = 796)
topFrame.grid(row = 0, columnspan = 6, sticky = W)

### 文字说明
currow = 0
Label(topFrame, text = "选择将要扫描的文件夹, 最多支持4个, 当选择删除重复文件时, 排在后面的文件将被删除").grid(row = currow, column = 0, columnspan = 6, sticky = W, padx = 7)

### 文件选择1
currow = currow + 1
Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 0)
Entry(topFrame, textvariable = pathlst[0], width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(0), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = pathlst[1],  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(1), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 5, padx = 7)

### 文件选择2
currow = currow + 1
Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 0)
Entry(topFrame, textvariable = pathlst[2], width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(2), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = pathlst[3],  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(3), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 5, padx = 7)


middleFrame = Frame(root, height = 200, width = 796)
middleFrame.grid(row = 1, columnspan = 6, sticky = W)

currow = 0
Label(middleFrame, text = "重复文件的操作方式").grid(row = currow, column = 0, padx = 7)
# currow = currow + 1
Radiobutton(middleFrame, text = "删除",  variable = radioVar, value = 1, command = lambda : targetDialogOpt(1)) \
.grid(row = currow, column = 1)
Radiobutton(middleFrame, text = "拷贝",  variable = radioVar, value = 2, command = lambda : targetDialogOpt(2)) \
.grid(row = currow, column = 2)

globalEntry = Entry(middleFrame, textvariable = pathlst[4], width = 40)
globalButton = Button(middleFrame, text = "选择", command = lambda : selectPath(4), width = 6, borderwidth = 0, fg = "blue")

btnRun = Button(middleFrame, text = "执行", borderwidth = 0, fg = "red", command = findRepeated)
btnRun.grid(row = currow, column = 5, padx = 10)

globalText = Text(root, width = 110, height = 37)
globalText.grid(row = 3, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()