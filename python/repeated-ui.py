from tkinter import *
from tkinter.filedialog import askdirectory
# def doRun():
# 	global root
# 	t = Label(root, text="执行扫描")
# 	t.pack()

# l1 = Label(root, text = "重复文件管理")
# l1.pack()

# btnRun = Button(root, text="执行", command = doRun)
# btnRun['width'] = 20
# btnRun.pack()

# Label(root, text = "账号: ").grid(row = 0, sticky = W)
# Entry(root).grid(row = 0, column = 1, sticky = E)
# Label(root, text = "密码: ").grid(row = 1, sticky = W)
# Entry(root).grid(row = 1, column = 1, sticky = E)
# Button(root, text = "登录").grid(row = 2, column = 1, sticky = E)

global globalEntry
global globalButton

def selectPath(p):
	_path = askdirectory()

	if p == 1:
		path1.set(_path)
	elif p == 2:
		path2.set(_path)
	elif p == 3:
		path3.set(_path)
	elif p == 4:
		path4.set(_path)
	elif p == 5:
		path5.set(_path)
	pass

def displayTargetDialog():
	global globalEntry
	global globalButton
	globalEntry.grid(row = 0, column = 3)
	globalButton.grid(row = 0, column = 4, padx = 7)
	

def destoryTargetDialog():
	global globalEntry
	global globalButton
	globalEntry.grid_remove() 
	globalButton.grid_remove()

def findRepeated():

root = Tk()
root.title("重复文件管理")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)

path1 = StringVar()
path2 = StringVar()
path3 = StringVar()
path4 = StringVar()
path5 = StringVar()

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
Entry(topFrame, textvariable = path1, width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(1), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = path2,  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(2), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 5, padx = 7)

### 文件选择2
currow = currow + 1
Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 0)
Entry(topFrame, textvariable = path3, width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(3), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = path4,  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(4), width = 6, borderwidth = 0, \
	fg = "blue").grid(row = currow, column = 5, padx = 7)


middleFrame = Frame(root, height = 200, width = 796)
middleFrame.grid(row = 1, columnspan = 6, sticky = W)

currow = 0
Label(middleFrame, text = "重复文件的操作方式").grid(row = currow, column = 0, padx = 7)
# currow = currow + 1
Radiobutton(middleFrame, text = "删除", variable = radioVar, value = 1, command = destoryTargetDialog) \
.grid(row = currow, column = 1)
Radiobutton(middleFrame, text = "拷贝", variable = radioVar, value = 2, command = displayTargetDialog) \
.grid(row = currow, column = 2)

globalEntry = Entry(middleFrame, textvariable = path5, width = 40)
globalButton = Button(middleFrame, text = "选择", command = lambda : selectPath(5), width = 6, borderwidth = 0, fg = "blue")

btnRun = Button(middleFrame, text = "执行", borderwidth = 0, fg = "red", command = findRepeated)
btnRun.grid(row = currow, column = 5, padx = 10)

Text(root, width = 110, height = 37).grid(row = 3, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()