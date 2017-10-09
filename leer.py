import os
import sys
from os import listdir
from os.path import isfile, isdir, join

def listdir_recurd(files_list, root, folder, checked_folders):

    if (folder != root):
        checked_folders.append(folder)

    for f in listdir(folder):
        d = join(folder, f)       

        if isdir(d) and d not in checked_folders:
            listdir_recurd(files_list, root, d, checked_folders)
        else:
            if isfile(d):  # si no hago esto, inserta en la lista el nombre de las carpetas ignoradas
                files_list.append(join(f))

    return files_list

def total_arch(folder,k):
    n=0
    for f in listdir(folder):   
        if f[2:11]==k:
            n=n+1

    return n



def borraraux():
    if(os.path.exists("r.jpg")):
        os.remove("r.jpg")          

    if(os.path.exists("0.jpg")):
        os.remove("0.jpg") 
        if(os.path.exists("1.jpg")):
            os.remove("1.jpg")  
            if(os.path.exists("2.jpg")):
                os.remove("2.jpg") 
                if(os.path.exists("3.jpg")):
                    os.remove("3.jpg")
                    if(os.path.exists("4.jpg")):
                        os,remove("4.jpg")

#print(total_arch("segmentada/","6ewy6.jpg"))