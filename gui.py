#ESO Manual AddOn Installer v0.2
#by Shane Ricci

#Import libraries

print('--------------------------------')
print('Begin startup.')
print('Initializing libraries.')

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from zipfile import ZipFile
from pathlib import Path
import shutil, os, stat, subprocess

print('Libraries initialized.')
print('Preparing initial functions.')

#Functions requiring early initialization

def getPath(file):
    #Function to convert environmental variables to useable paths and swap forward/back slashes
    reslash = file.replace("/","\\")
    expand = os.path.expandvars(reslash)
    return expand

def findSettings(stringToFind, file):
    #Function to find a given string within a file and return the contents of the line minus the string
    importPath = getPath(r'c:\\Users\\$USERNAME\\')
    with open(file, "r+") as openFile:
        lines = openFile.read().splitlines()
    for lineCheck in lines:
        if stringToFind in lineCheck:
            importPath = lineCheck.replace(stringToFind, '')
            return importPath
        else:
            continue
    print('--------------------------------')
    print('WARNING: Some settings failed to import.')
    print('Please delete paths.txt and restart app.')
    print('--------------------------------')
    return importPath

print('Initial functions prepared.')
print('Establishing variables.')

#Initialize variables and GUI

window = tk.Tk()
window.title('ESO')
window.geometry("200x190")
filename = ''
sett_file = Path("paths.txt")
dl_path = r'c:\\Users\\$USERNAME\\Downloads\\'
dl_path = getPath(dl_path)
ao_path = r'c:\\Users\\$USERNAME\\Documents\\Elder Scrolls Online\\live\\AddOns\\'
ao_path = getPath(ao_path)
base_path = r'c:\\Users\\$USERNAME\\'
base_path = getPath(base_path)
end_slashes = r'\\'

print('Variables established.')
print('Loading functions.')

#File browser function

def browseFiles():
    global filename
    print('Begin file unzip process.')
    print('--------------------------------')
    filename = filedialog.askopenfilename(initialdir = dl_path,
                                          title = "Select a File",
                                          filetypes = (("Zip files", "*.zip"),
                                                       ("all files", "*.*")))
    if (len(filename) == 0):
        print('File selection cancelled.')
        print('--------------------------------')
        return
    else:
        filetrim = Path(filename).name
        print(filetrim + ' is selected.')
        unzip()
        print(filetrim + ' was unzipped successfully.')
        print('--------------------------------')
        return

#Unzip function

def unzip():
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(dl_path)

#File movement function

def filemv():
    global filename
    print('Begin file movement process.')
    print('--------------------------------')
    filename = filedialog.askdirectory(initialdir = dl_path,
                                            title = "Select a Folder")
    if (len(filename) == 0):
        print('File selection cancelled.')
        print('--------------------------------')
        return
    else:
        folder = Path(filename).name
        final = ao_path + folder
        print('Moving ' + folder + ' to ' + final)
        shutil.copytree(filename, final, dirs_exist_ok = True)
        print(folder + ' installed.')
        shutil.rmtree(filename)
        print(folder + ' deleted.')
        print('--------------------------------')
        return

#Manual install folder function

def openFolders():
    dl_upd = dl_path.replace("\\\\","\\")
    cmd_dl = r'explorer "' + dl_upd + r'"'
    ao_upd = ao_path.replace("\\\\","\\")
    cmd_ao = r'explorer "' + ao_upd + r'"'
    subprocess.Popen(cmd_dl, shell=True)
    subprocess.Popen(cmd_ao, shell=True)
    print('Opened Downloads & AddOns folders.')
    print('--------------------------------')
    return

#Settings window function

def settings():
    print('Generating Settings window.')
    settings_window = Toplevel(window)
    settings_window.title('Settings')
    settings_window.geometry("230x140")
    
    sett_button_dlpath = Button(settings_window,
                                text = "Downloads",
                                command = dlPath)

    sett_button_aopath = Button(settings_window,
                                text = "AddOns",
                                command = aoPath)

    sett_button_exit = Button(settings_window,
                              text = "Return",
                              command = settings_window.destroy)
    
    sett_button_dlpath.grid(column = 1, row = 1, padx = 2, pady = 2)
    sett_button_aopath.grid(column = 1, row = 2, padx = 2, pady = 2)
    sett_button_exit.grid(column = 1, row = 3, padx = 2, pady = 2)
    
    label_sett_title = Label(settings_window, text = "  Settings")
    label_sett_title.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)
    label_sett_dlpath = Label(settings_window, text = "Change Downloads Path: ")
    label_sett_dlpath.grid(column = 0, row = 1, padx = 2, pady = 2)
    label_sett_aopath = Label(settings_window, text = "Change AddOns Path: ")
    label_sett_aopath.grid(column = 0, row = 2, padx = 2, pady = 2)
    print('Settings window generated.')
    print('--------------------------------')
    return

def dlPath():
    #Open file dialog to change Downloads path
    global dl_path
    path = filedialog.askdirectory(initialdir = base_path,
                                        title = "Select a Folder")
    if (len(path) == 0):
        print('File selection cancelled.')
        print('--------------------------------')
        return
    else:
        old_path = dl_path
        dl_path = path.replace("/",r"\\")
        dl_path += end_slashes
        updatePath('DL_PATH=', old_path, dl_path, sett_file)
        print('New Downloads Path: ' + dl_path)
        print('--------------------------------')
    return

def aoPath():
    #Open file dialog to change AddOns path
    global ao_path
    path = filedialog.askdirectory(initialdir = base_path,
                                        title = "Select a Folder")
    if (len(path) == 0):
        print('File selection cancelled.')
        print('--------------------------------')
        return
    else:
        old_path = ao_path
        ao_path = path.replace("/",r"\\")
        ao_path += end_slashes
        updatePath('AO_PATH=', old_path, ao_path, sett_file)
        print('New AddOns Path: ' + ao_path)
        print('--------------------------------')
    return

def checkSettingsFile():
    #Function to check for existence of Settings file and, if it exists, import paths
    global dl_path, ao_path
    if sett_file.is_file():
        #File exists, import settings
        print('Settings file found.')
        dl_path = findSettings(r'DL_PATH=', sett_file)
        ao_path = findSettings(r'AO_PATH=', sett_file)
        return
    else:
        #File doesn't exist, create and write default values
        print('No settings file detected.')
        settings = open(sett_file,"w+")
        settings.write("DL_PATH=" + dl_path + "\n")
        settings.write("AO_PATH=" + ao_path + "\n")
        settings.close()
        print('Settings file created.')
        return

def updatePath(setting, old_path, new_path, file):
    count = 0
    with open(file, "r+") as openFile:
        lines = openFile.read().splitlines()
    for lineCheck in lines:
        if setting in lineCheck:
            lines[count] = lineCheck.replace(old_path, new_path)
        else:
            count += 1
            continue
    lines_str = "\n".join(lines)
    openFile = open(file, "wt")
    openFile.write(lines_str)
    openFile.close()
    print('Settings file modified.')
    return

print('Functions loaded.')
print('Generating GUI.')

#Initialize GUI buttons

button_unzip = Button(window,
                      text = "Unzip",
                      command = browseFiles)

button_install = Button(window,
                        text = "Install",
                        command = filemv)

button_manual = Button(window,
                        text = "Manual",
                        command = openFolders)

button_settings = Button(window,
                         text = "Settings",
                         command = settings)

button_exit = Button(window,
                     text = "Exit",
                     command = window.destroy)

#Layout 'window' buttons

button_unzip.grid(column = 1, row = 1, padx = 2, pady = 2)
button_install.grid(column = 1, row = 2, padx = 2, pady = 2)
button_manual.grid(column = 1, row = 3, padx = 2, pady = 2)
button_settings.grid(column = 1, row = 4, padx = 2, pady = 2)
button_exit.grid(column = 1, row = 5, padx = 2, pady = 2)

#Labels for 'window'

label_greeting = Label(window, text = " ESO Manual AddOn Installer")
label_greeting.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

label_start = Label(window, text = "Unzip: ")
label_start.grid(column = 0, row = 1, padx = 2, pady = 2)

label_end = Label(window, text = "Move Folder: ")
label_end.grid(column = 0, row = 2, padx = 2, pady = 2)

label_manual = Label(window, text = "Manual Shortcut: ")
label_manual.grid(column = 0, row = 3, padx = 2, pady = 2)

label_settings = Label(window, text = "Settings: ")
label_settings.grid(column = 0, row = 4, padx = 2, pady = 2)

print('GUI generated.')
print('Importing settings.')

#Check settings

checkSettingsFile()

#GUI mainloop

print('Settings imported.')
print('Startup complete.')
print('--------------------------------')

window.mainloop()
