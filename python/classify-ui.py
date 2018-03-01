import hashlib
import sys
import os
import shutil
import time
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename

global global_ext_dict
global global_check_var_list
global global_ext_copy_list
global global_check_button_list
global global_check_button_all

global_ext_dict = dict()
global_ext_copy_list = []
global_check_var_list = []
global_check_button_list = []
global_check_button_all = None

def selectPath():
    path = askdirectory()
    scan_path_var.set(path)
    pass

def print_to_text(s):
    global_text.insert(0.0, s)
    time.sleep(0.02)
    global_text.update()

def get_relavte_path(fname):
    dirlen = len(scan_path_var.get()) + 1
    name   = fname[dirlen:]
    return name

def clear_global_vars():
    global global_ext_dict, global_ext_copy_list
    global global_check_var_list, global_check_button_list
    global_ext_dict.clear()
    global_ext_copy_list.clear()
    global_check_button_list.clear()
    for l in global_check_var_list:
        l.set("")

def proc_check_button_all():
    global global_check_button_list
    for btn in global_check_button_list:
        if check_button_all_var.get() == 1:
            btn.select()
        else:
            btn.deselect()
        pass
    pass
def display_ext_checkbox(ext_list):
    global global_check_var_list, global_check_button_list, global_check_button_all
    row = 0
    column = 0
    for l in range(len(ext_list)):
        btn = Checkbutton(class_frame, text = ext_list[l], variable = global_check_var_list[l], onvalue = ext_list[l], \
            offvalue = "")
        btn.grid(row = row, column = column, sticky = W, padx = 3)
        global_check_button_list.append(btn)

        column = column + 1
        if(column == 13):
            row = row + 1
            column = 0
        pass
    pass
    global_check_button_all = Checkbutton(class_frame, text = "全选", variable = check_button_all_var, command = proc_check_button_all)
    global_check_button_all.grid(row = row, column = column, sticky = W, padx = 3)

def display_frame_things():
    class_frame.grid(row = 1, columnspan = 12, sticky = W, pady = 7, padx = 6)
    copy_frame.grid(row = 2, columnspan = 6, sticky = W, pady = 1, padx = 6)
    textFrame.grid(row = 3, columnspan = 6, sticky = W)

def destroy_check_button():
    global global_check_button_list, global_check_button_all
    for btn in global_check_button_list:
        if btn:
            btn.destroy()
    if global_check_button_all:
        global_check_button_all.destroy()
        global_check_button_all = None

def display_file_statistics(ext_list):
    global global_ext_dict
    print_str = ""
    for ext in ext_list:
        print_str = "%-6s : %d \n" % (ext, len(global_ext_dict[ext]))
        print_to_text(print_str)
    pass
def start_scan():
    global global_ext_dict
    ext_list = []
    destroy_check_button()
    clear_global_vars()
    directory = scan_path_var.get()
    for root, dirs, files in os.walk(directory):
        for f in files:
            (name, ext) = os.path.splitext(f)
            if ext == "":
                ext = ".nil"
            if ext not in ext_list:
                ext_list.append(ext)
                global_ext_dict[ext] = []
            global_ext_dict[ext].append(os.path.join(root, f))
        pass
    pass

    display_ext_checkbox(ext_list)
    display_frame_things()
    display_file_statistics(ext_list)

def copy_target(target_dir, ext):
    global global_ext_dict, glo
    f_list = global_ext_dict[ext];

    for f in f_list:
        try:
            shutil.move(f, target_dir)
            print_to_text("move %s to %s\n" % (get_relavte_path(f), target_dir))
        except Exception as e:
            print_to_text(str(e) + "\n")
        finally:
            pass
    pass

def start_copy():
    global global_check_var_list
    directory = scan_path_var.get()

    for l in global_check_var_list:
        ext = l.get()
        if ext:
            target_dir = os.path.join(directory, "copy_" + ext[1:])
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            copy_target(target_dir, ext)
        pass
    pass
root = Tk()
root.title("文件分类")
root.geometry('800x600+250+80')
root.maxsize(800, 600)
root.minsize(800, 600)

scan_path_var = StringVar()
check_button_var = IntVar()
check_button_all_var = IntVar()

for i in range(128):
    global_check_var_list.append(StringVar())

### 000000
scan_frame = Frame(root, width = 796)
scan_frame.grid(row = 0, columnspan = 6, sticky = W, pady = 7)

Label(scan_frame, text = "路径", width = 6).grid(row = 0, column = 0)
Entry(scan_frame, textvariable = scan_path_var, width = 68).grid(row = 0, column = 1)
Button(scan_frame, text = "选择", command = selectPath, width = 6, borderwidth = 0, \
    fg = "blue").grid(row = 0, column = 2, padx = 7)
Button(scan_frame, text = "开始扫描", command = start_scan, width = 6, borderwidth = 0, \
    fg = "red").grid(row = 0, column = 3)

class_frame = Frame(root, width = 796)
### 222222
copy_frame = Frame(root, width = 796)

Label(copy_frame, text = "选择文件类型, 拷贝到对应的文件夹中. 该程序会在当前文件夹下新建对应的目录") \
.grid(row = 0, column = 0)
Button(copy_frame, text = "开始拷贝", command = start_copy, width = 6, borderwidth = 0, \
    fg = "red").grid(row = 0, column = 3, padx = 7)

### 333333
textFrame = Frame(root, height = 200, width = 796)

global_text = Text(textFrame, width = 110, height = 37)
global_text.grid(row = 0, column = 0, columnspan = 6, ipadx = 10, ipady = 10)

root.mainloop()