import hashlib
import sys
import os
import shutil
import time
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
global global_copy_entry
global global_copy_button
global global_text
global global_path_list
global global_indicate_label
global global_current_label
global global_md5_list
global global_copy_directory
global global_del_indicate

global_path_list = []
global_md5_list = []
global_del_indicate = False

def print_cur_file(directory, file):
    """显示当前处理的文件"""
    global global_current_label
    dirlen = len(directory) + 1
    name   = file[dirlen:]
    global_current_label['text'] = name
    time.sleep(0.02)
    global_current_label.update()

def print_to_text(s):
    """显示信息到text"""
    global global_text
    global_text.insert(END, s)
    time.sleep(0.02)
    global_text.update()

def calc_md5(fname):
    md5 = hashlib.md5()
    with open(fname, 'rb') as fp:
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
    global global_del_indicate
    global global_copy_directory

    if global_del_indicate is False:
        count = 1
        target_name = os.path.join(global_copy_directory, f)
        while os.path.exists(target_name):
            (name, ext) = os.path.splitext(f)
            ends = '_%d' % count
            count = count + 1
            if name.endswith(ends):
                f = '%s%d%s' % (name[0:-1], count, ext)
            else:
                f = '%s_%d%s' % (name, count, ext)
            target_name = os.path.join(global_copy_directory, f)
        else:
            print_to_text('move file %s to %s as %s\n' % (fname, global_copy_directory, f))
            shutil.move(fname, target_name)
    else:
        print_to_text('delete file %s\n' % fname)
        os.remove(fname)

def find_repeated(directory):
    global global_md5_list
    for root, dirs, files in os.walk(directory):
        for f in files:
            fname = os.path.join(root, f)
            print_cur_file(directory, fname)
            md5hex = calc_md5(fname)
            if md5hex not in global_md5_list:
                global_md5_list.append(md5hex)
            else:
                repeated_opts(f, fname)
            pass
        pass
    pass

def selectPath(p):
    global global_path_list
    _path = askdirectory()
    global_path_list[p].set(_path)

def targetDialogOpt(opt):
    global global_copy_entry, global_copy_button, global_del_indicate, \
    global_copy_directory, global_del_indicate

    global_copy_directory = ''
    if opt == 2:
        global_copy_entry.grid(row = 0, column = 3)
        global_copy_button.grid(row = 0, column = 4, padx = 7)
        global_del_indicate = False
    elif opt == 1:
        global_copy_entry.grid_remove() 
        global_copy_button.grid_remove()
        global_del_indicate = True

def print_start_label():
    """显示开始执行"""
    global global_indicate_label
    global_indicate_label['text'] = "执行中...."

def print_end_label():
    """显示执行完成"""
    global global_indicate_label
    global_indicate_label['text'] = "执行完成"

def empty_text():
    """清空文本显示"""
    global global_text
    global_text.delete(0.0, END)

def show_info(s):
    """显示提示信息"""
    showinfo(message = s)

def init_repeated_copy_dir():
    """初始化重复文件拷贝的目的地"""
    global global_copy_directory, global_del_indicate
    global_copy_directory = global_path_list[4].get()
    if global_del_indicate == False and global_copy_directory == "":
        show_info("选择删除,或指定拷贝文件的目录")
        return False
    return True

def empty_md5_list():
    """清空存放文件md5值的列表"""
    global global_md5_list
    global_md5_list.clear()

def findRepeated():
    """查找重复文件的总入口"""
    global global_path_list
    if True == init_repeated_copy_dir():
        print_start_label()
        empty_text()
        empty_md5_list()
        for i in range(4):
            path = global_path_list[i].get()
            if path:
                find_repeated(path)
            pass
        pass
        print_end_label()
    pass

root = Tk()
root.title("重复文件管理")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)
for i in range(5):
    global_path_list.append(StringVar())

radioVar = IntVar()
###
### 目录选择FRAME
### 
topFrame = Frame(root, height = 200, width = 796)
topFrame.grid(row = 0, columnspan = 6, sticky = W)

### 文字说明
currow = 0
Label(topFrame, text = "选择将要扫描的文件夹, 最多支持4个, 当选择删除重复文件时, 排在后面的文件将被删除").grid(row = currow, column = 0, columnspan = 6, sticky = W, padx = 7)

### 文件选择1
currow = currow + 1
Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 0)
Entry(topFrame, textvariable = global_path_list[0], width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(0), width = 6, borderwidth = 0, \
    fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = global_path_list[1],  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(1), width = 6, borderwidth = 0, \
    fg = "blue").grid(row = currow, column = 5, padx = 7)

### 文件选择2
currow = currow + 1
Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 0)
Entry(topFrame, textvariable = global_path_list[2], width = 40).grid(row = currow, column = 1)
Button(topFrame, text = "选择", command = lambda : selectPath(2), width = 6, borderwidth = 0, \
    fg = "blue").grid(row = currow, column = 2, padx = 7)

Label(topFrame, text = "路径", width = 6).grid(row = currow, column = 3)
Entry(topFrame, textvariable = global_path_list[3],  width = 40).grid(row = currow, column = 4)
Button(topFrame, text = "选择", command = lambda : selectPath(3), width = 6, borderwidth = 0, \
    fg = "blue").grid(row = currow, column = 5, padx = 7)


###
### 操作方式FRAME
### 
middleFrame = Frame(root, height = 200, width = 796)
middleFrame.grid(row = 1, columnspan = 6, sticky = W)

currow = 0
Label(middleFrame, text = "重复文件的操作方式").grid(row = currow, column = 0, padx = 7)
# currow = currow + 1
Radiobutton(middleFrame, text = "删除",  variable = radioVar, value = 1, command = lambda : targetDialogOpt(1)) \
.grid(row = currow, column = 1)
Radiobutton(middleFrame, text = "拷贝",  variable = radioVar, value = 2, command = lambda : targetDialogOpt(2)) \
.grid(row = currow, column = 2)

global_copy_entry = Entry(middleFrame, textvariable = global_path_list[4], width = 40)
global_copy_button = Button(middleFrame, text = "选择", command = lambda : selectPath(4), width = 6, borderwidth = 0, fg = "blue")

btnRun = Button(middleFrame, text = "执行", borderwidth = 0, fg = "red", command = findRepeated)
btnRun.grid(row = currow, column = 5, padx = 10)

global_indicate_label = Label(middleFrame)
global_indicate_label.grid(row = currow, column = 6)

###
### 显示当前处理的文件的FRAME
### 

buttomFrame = Frame(root, height = 200, width = 796)
buttomFrame.grid(row = 2, columnspan = 6, sticky = W)
global_current_label = Label(buttomFrame)
global_current_label.grid(row = 0, column = 0, columnspan = 6, sticky = W, padx = 10)


###
### text
### 
textFrame = Frame(root, height = 200, width = 796)
textFrame.grid(row = 3, columnspan = 6, sticky = W)

global_text = Text(textFrame, width = 110, height = 37)
global_text.grid(row = 0, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()