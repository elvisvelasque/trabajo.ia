# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:31:33 2017

@Antoniouthor: Antonio
"""

from PIL import Image
import time 
import numpy as np
import os
import glob, os

archivo=0
directory='C:/Users/Antonio/Desktop/ia.trabajo'

for i in os.listdir(directory):
    print(i)
    for c in i:
        if c == ".":
            archivo=1

    if archivo==0:
        for j in os.listdir(directory+"/"+i):
            print(j)
            for c in i:
                if c == ".":
                    archivo=1

            if archivo==0:
                for k in os.listdir(directory+"/"+i+"/"+j):
                    os.remove(directory+"/"+i+"/"+j+"/"+k)

