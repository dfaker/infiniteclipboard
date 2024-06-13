

import tkinter as tk
from tkinter import filedialog

import threading
import ctypes
from ctypes import wintypes
import pythoncom
import win32clipboard
import os
import random
import time
import keyboard
import json


class DROPFILES(ctypes.Structure):
    _fields_ = (('pFiles', wintypes.DWORD),
                ('pt',     wintypes.POINT),
                ('fNC',    wintypes.BOOL),
                ('fWide',  wintypes.BOOL))

def clip_files(file_list):
    offset = ctypes.sizeof(DROPFILES)
    length = sum(len(p) + 1 for p in file_list) + 1
    size = offset + length * ctypes.sizeof(ctypes.c_wchar)
    buf = (ctypes.c_char * size)()
    df = DROPFILES.from_buffer(buf)
    df.pFiles, df.fWide = offset, True
    for path in file_list:
        array_t = ctypes.c_wchar * (len(path) + 1)
        path_buf = array_t.from_buffer(buf, offset)
        path_buf.value = path
        offset += ctypes.sizeof(path_buf)
    stg = pythoncom.STGMEDIUM()    
    stg.set(pythoncom.TYMED_HGLOBAL, buf)
    win32clipboard.OpenClipboard()
    try:
        res = win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, stg.data)
        print(res)
    except Exception as e:
        print(e)
    finally:
        win32clipboard.CloseClipboard()



allimages = []
images = []


index=0
def getimage():
    global index
    try:
        nextim = images[index % len(images)]
        index+=1
        return nextim
    except:
        pass

def imagesupply():
    while 1:
        i = getimage()
        print(i)
        if i is not None:
            clip_files([os.path.abspath(i)])
            while 1:
                if keyboard.is_pressed('ctrl+v'):
                    while keyboard.is_pressed('ctrl+v'):
                        pass
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.CloseClipboard()
                    break

imageworker = threading.Thread(target=imagesupply,daemon=True)
imageworker.start()

root = tk.Tk()

gif_var = tk.BooleanVar()
jpg_var = tk.BooleanVar()
png_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()

gif_var.set(True)
jpg_var.set(True)
png_var.set(True)
mp4_var.set(True)

def select_directory():
    directory = filedialog.askdirectory()
    if directory:  # If a directory was selected
        directory_label.config(text=directory)  # Update the label
        allimages.clear()
        for r,_,fl in os.walk(directory):
            for f in fl:
                p = os.path.join(r,f)
                if any(p.endswith(x) for x in ['mp4','']):
                    allimages.append(p)
                    print(p)
        filterresults()


def shuffle_paths():
    random.shuffle(images)

def filterresults(*args):

    endings = {
        'gif':gif_var,
        'jpg':jpg_var,
        'jpeg':jpg_var,
        'png':png_var,
        'mp4':mp4_var
    }
    endings = [x for x,y in endings.items() if y.get()]
    print(endings)
    images.clear()
    for i in [x for x in allimages if any([x.upper().endswith(t.upper()) for t in endings])]:
        images.append(i)


root.title("Inifinite Clipboard")
root.geometry('600x150+50+50')  # Places the window at position (50,50)
root.resizable(False, False)  # Prevent resizing for more compactness

# Button to select the directory
select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack(side='top', fill='x', padx=5, pady=5)

# Label to display the current directory
directory_label = tk.Label(root, text="No directory selected", anchor="center")
directory_label.pack(side='top', fill='x', padx=5, pady=5)


gif_check = tk.Checkbutton(root, text="GIF", variable=gif_var)
jpg_check = tk.Checkbutton(root, text="JPG", variable=jpg_var)
png_check = tk.Checkbutton(root, text="PNG", variable=png_var)
mp4_check = tk.Checkbutton(root, text="MP4", variable=mp4_var)

select_dir_button = tk.Button(root, text="Shuffle", command=shuffle_paths)
select_dir_button.pack(side='bottom', fill='x', padx=5, pady=5)

checkbox_frame = tk.Frame(root)
checkbox_frame.pack(side='top', fill='x', padx=5, pady=5)
gif_check.pack(side='left', expand=True)
jpg_check.pack(side='left', expand=True)
png_check.pack(side='left', expand=True)
mp4_check.pack(side='left', expand=True)

gif_var.trace('w',filterresults)
jpg_var.trace('w',filterresults)
png_var.trace('w',filterresults)
mp4_var.trace('w',filterresults)

root.mainloop()