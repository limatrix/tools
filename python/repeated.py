import hashlib
import sys
import os
import shutil
import getopt

global_list = []
global_repeated = ''
global_delete = False

def usage():
    print u'-h, --help'
    print u'-s, --source'
    print u'-d, --delete'

def calc_md5(fname):
    md5 = hashlib.md5()
    with open(fname, 'rb') as fp:
        print 'checking %s' % fname
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
            print 'move %s to %s as %s' % (fname, global_repeated, f)
            shutil.move(fname, target_name)
    else:
        print 'delete %s' % fname
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

def main():
    help = False
    directory = ''
    input_file = ''

    global global_repeated
    global global_delete

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dhs:f:', ['delete', 'help', 'source=', 'file='])

        for opt, arg in opts:
            if opt in ('-d', '--delete'):
                global_delete = True
            elif opt in ('-s', '--source'):
                directory = arg
            elif opt in ('-h', '--help'):
                help = True
            elif opt in ('-f', '--file'):
                input_file = arg
            pass
        pass

        if (not directory and not input_file) or help:
            usage()
            return

        print input_file
        if input_file:
            for directory in open(input_file):
                print directory
                find_repeated(directory)
        else:
            find_repeated(directory)

    except:
        usage()

if __name__ == '__main__':
    main()