import hashlib
import sys
import os
import shutil
import time
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
global global_copy_entry
global global_copy_button
global global_hash_entry
global global_hash_button
global global_text
global global_path_list
global global_current_label
global global_md5_list
global global_copy_directory
global global_del_indicate
global global_file_ds
global global_validate_indicate
global global_current_directory

global_path_list = []
global_md5_list = []
global_del_indicate = False
global_file_ds = None
global_validate_indicate = None

def print_to_current_label(directory, file):
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
    global_text.insert(0.0, s)
    time.sleep(0.02)
    global_text.update()

def print_to_file(directory, fname, md5hex):
    """将信息写到文件"""
    global global_file_ds
    dirlen = len(directory) + 1
    name   = fname[dirlen:]
    global_file_ds.write(md5hex + "," + name + "\n")

def get_relavte_path(fname):
    """截取绝对路径为相对路径"""
    global global_current_directory
    dirlen = len(global_current_directory) + 1
    name   = fname[dirlen:]
    return name

def print_repeated_summary(sum_count, opt_count):
    """重复文件扫描完成后打印信息"""
    global global_del_indicate
    temp_str = ""
    return_str = "共扫描文件: %d个\n" % sum_count

    if global_del_indicate is True:
        temp_str = "共删除文件: %d个\n" % opt_count
    else:
        temp_str = "共拷贝文件: %d个\n" % opt_count
    return_str = return_str +  temp_str
    print_to_text(return_str)

def remove_empty_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            workpath = os.path.join(root, name)
            if not os.listdir(workpath):
                print("del path %s\n" % workpath)
                os.removedirs(workpath)
            pass
        pass
    pass

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
            print_to_text('move file %s to %s as %s\n' % (get_relavte_path(fname), global_copy_directory, f))
            shutil.move(fname, target_name)
    else:
        print_to_text('deleting %s\n' % get_relavte_path(fname))
        os.remove(fname)
    pass

def find_repeated(directory):
    global global_md5_list
    global global_current_directory
    global_current_directory = directory

    sum_count = 0
    opt_count = 0

    for root, dirs, files in os.walk(directory):
        for f in files:
            fname = os.path.join(root, f)
            print_to_current_label(directory, fname)
            md5hex = calc_md5(fname)
            sum_count = sum_count + 1
            if md5hex not in global_md5_list:
                if check_button_var.get() != 1:
                    global_md5_list.append(md5hex)
                pass
            else:
                repeated_opts(f, fname)
                opt_count = opt_count + 1
            pass
        pass
    return (sum_count, opt_count)

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
            print_to_current_label(directory, fname)
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
            print_to_current_label(directory, fname)
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
        return_str = return_str + "  " + get_relavte_path(l) + "\n"

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

def load_hash_file(file):
    global global_md5_list
    for line in open(file):
        lst = line.split(",")
        global_md5_list.append(lst[0])
    pass

def findRepeated():
    """查找重复文件的总入口"""
    global global_path_list, global_md5_list
    sum_count = 0
    opt_count = 0
    if True == init_repeated_copy_dir():
        print_start_label()
        empty_text()
        empty_md5_list()

        if check_button_var.get() == 1:
            hash_file = global_hash_file.get()
            load_hash_file(hash_file)

        for i in range(4):
            path = global_path_list[i].get()
            if path:
                (a,b) = find_repeated(path)
                sum_count = sum_count + a
                opt_count = opt_count + b
                remove_empty_directory(path)
            pass
        pass
        print_end_label()
        empty_all_path()
    pass
    print_repeated_summary(sum_count, opt_count)

def check_button_proc():
    opt = check_button_var.get()
    if opt == 1:
        global_hash_entry.grid(row = 0, column = 2)
        global_hash_button.grid(row = 0, column = 3, padx = 7)
    elif opt == 0:
        global_hash_entry.grid_remove() 
        global_hash_button.grid_remove()
    pass

def selectfile(opt):
    file = askopenfilename()
    global_hash_file.set(file)

root = Tk()
root.title("重复文件管理")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)
for i in range(6):
    global_path_list.append(StringVar())

repeat_radio_var = IntVar()
validate_radio_var = IntVar()
check_button_var = IntVar()
global_hash_file = StringVar()

frame_cur_row = 0
###
### HASH选择FRAME
###
hashFrame = Frame(root, height = 200, width = 796)
hashFrame.grid(row = frame_cur_row, columnspan = 6, sticky = W)

Label(hashFrame, text = "使用校验文件作为重复检查基准").grid(row = 0, column = 0, sticky = W, padx = 7, pady = 2)
Checkbutton(hashFrame, variable = check_button_var, command = check_button_proc).grid(row = 0, column = 1, sticky = W, padx = 7, pady = 2)
global_hash_entry = Entry(hashFrame, textvariable = global_hash_file, width = 40)
global_hash_button = Button(hashFrame, text = "选择", command = lambda : selectfile(1), width = 6, borderwidth = 0, fg = "blue")

###
### 目录选择FRAME
### 

frame_cur_row = frame_cur_row + 1
topFrame = Frame(root, height = 200, width = 796)
topFrame.grid(row = frame_cur_row, columnspan = 6, sticky = W)

### 文字说明
currow = 0
Label(topFrame, text = "选择将要扫描的文件夹, 最多支持4个文件夹. 按文件夹顺序扫描, 如果选择删除重复文件, \
排在后面的文件将被删除.").grid(row = currow, column = 0, columnspan = 6, sticky = W, padx = 7, pady = 5)

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
frame_cur_row = frame_cur_row + 1
middleFrame = Frame(root, height = 200, width = 796)
middleFrame.grid(row = frame_cur_row, columnspan = 6, sticky = W)

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
frame_cur_row = frame_cur_row + 1
buttomFrame = Frame(root, height = 200, width = 796)
buttomFrame.grid(row = frame_cur_row, columnspan = 6, sticky = W)
global_current_label = Label(buttomFrame)
global_current_label.grid(row = 0, column = 0, columnspan = 6, sticky = W, padx = 7)


###
### text
### 
frame_cur_row = frame_cur_row + 1
textFrame = Frame(root, height = 200, width = 796)
textFrame.grid(row = frame_cur_row, columnspan = 6, sticky = W)

global_text = Text(textFrame, width = 110, height = 37)
global_text.grid(row = 0, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()