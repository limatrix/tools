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
global global_current_label
global global_md5_list
global global_copy_directory
global global_del_indicate
global global_file_ds
global global_validate_indicate

global_path_list = []
global_md5_list = []
global_del_indicate = False
global_file_ds = None
global_validate_indicate = None

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

def empty_all_path():
    global global_path_list
    for l in global_path_list:
        l.set("")
    pass
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

def validationOpt(opt):
    global global_validate_indicate
    global_validate_indicate = opt

def print_to_file(directory, fname, md5hex):
    global global_file_ds
    dirlen = len(directory) + 1
    name   = fname[dirlen:]
    global_file_ds.write(md5hex + "," + name + "\n")

def generate_validate(directory):
    global global_file_ds
    count = 0
    global_file_ds = open(directory + "/hash.db", "w+")
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == "hash.db":
                continue
            fname = os.path.join(root, f)
            count = count + 1
            print_cur_file(directory, fname)
            md5hex = calc_md5(fname)
            print_to_file(directory, fname, md5hex)
        pass
    pass
    global_file_ds.close()
    global_file_ds = None
    print_str = "目录:     " + directory + "\n" \
                "文件总数: " + str(count) + "\n" \
                "校验文件: " + "hash.db\n"
    print_to_text(print_str)

def get_relavte_path(directory, fname):
    dirlen = len(directory) + 1
    name   = fname[dirlen:]
    return name

def proc_validate(directory):
    dictionary = {}
    rlist = []
    fset = set()
    rset = set()
    for line in open(directory + "/hash.db"):
        lst = line.split(",")
        dictionary[lst[0]] = lst[1]
        fset.add(lst[0])

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == "hash.db":
                continue
            fname = os.path.join(root, f)
            print_cur_file(directory, fname)
            md5hex = calc_md5(fname)
            rset.add(md5hex)
            if md5hex not in dictionary:
                rlist.append(fname)
        pass
    pass

    # hash.db里有, 文件夹里没有的
    temp1 = list(fset.difference(rset))

    # 文件夹里有, hash.db里没有的
    temp2 = list(rset.difference(fset))

    return_str = "文件夹里丢失的文件:\n\n"
    for l in temp1:
        return_str = return_str + "  " + dictionary[l]
    return_str = return_str + "\n文件夹里新增的文件:\n\n"
    for l in rlist:
        return_str = return_str + "  " + get_relavte_path(directory, l) + "\n"

    print_to_text(return_str)

def validate():
    global global_validate_indicate
    print_start_label()
    empty_text()
    
    if global_validate_indicate == 1:
        for i in range(4):
            path = global_path_list[i].get()
            if path:
                generate_validate(path)
            pass
        pass
    elif global_validate_indicate == 2:
        for i in range(4):
            path = global_path_list[i].get()
            if path:
                proc_validate(path)
            pass
        pass
    print_end_label()
    empty_all_path()

def print_start_label():
    """显示开始执行"""
    # global_current_label['text'] = "执行中...."

def print_end_label():
    """显示执行完成"""
    global global_current_label
    global_current_label['text'] = "执行完成"

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

def empty_path_list():
    """清空存放path的列表"""
    global global_path_list
    global_path_list.clear()

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
        empty_all_path()
    pass


root = Tk()
root.title("重复文件管理")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)
for i in range(6):
    global_path_list.append(StringVar())

repeat_radio_var = IntVar()
validate_radio_var = IntVar()
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
Label(middleFrame, text = "重复文件的操作方式").grid(row = currow, column = 0, padx = 7, sticky = W)

Radiobutton(middleFrame, text = "删除",  variable = repeat_radio_var, value = 1, command = lambda : targetDialogOpt(1)) \
.grid(row = currow, column = 1, sticky = W)
Radiobutton(middleFrame, text = "拷贝",  variable = repeat_radio_var, value = 2, command = lambda : targetDialogOpt(2)) \
.grid(row = currow, column = 2, sticky = W)

global_copy_entry = Entry(middleFrame, textvariable = global_path_list[4], width = 40)
global_copy_button = Button(middleFrame, text = "选择", command = lambda : selectPath(4), width = 6, borderwidth = 0, fg = "blue")

btnRun = Button(middleFrame, text = "执行", borderwidth = 0, fg = "red", command = findRepeated)
btnRun.grid(row = currow, column = 5, padx = 10, sticky = W)

#
currow = currow + 1
Label(middleFrame, text = "完整性校验").grid(row = currow, column = 0, padx = 7, sticky = W)

Radiobutton(middleFrame, text = "生成校验文件",  variable = validate_radio_var, value = 1, command = lambda : validationOpt(1)) \
.grid(row = currow, column = 1, sticky = W)
Radiobutton(middleFrame, text = "检查完整性",  variable = validate_radio_var, value = 2, command = lambda : validationOpt(2)) \
.grid(row = currow, column = 2, sticky = W)

btnRun = Button(middleFrame, text = "执行", borderwidth = 0, fg = "red", command = validate)
btnRun.grid(row = currow, column = 5, padx = 10, sticky = W)



###
### 显示当前处理的文件的FRAME
### 

buttomFrame = Frame(root, height = 200, width = 796)
buttomFrame.grid(row = 2, columnspan = 6, sticky = W)
global_current_label = Label(buttomFrame)
global_current_label.grid(row = 0, column = 0, columnspan = 6, sticky = W, padx = 7)


###
### text
### 
textFrame = Frame(root, height = 200, width = 796)
textFrame.grid(row = 3, columnspan = 6, sticky = W)

global_text = Text(textFrame, width = 110, height = 37)
global_text.grid(row = 0, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()