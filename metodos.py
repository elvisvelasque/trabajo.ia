# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:31:33 2017

@Antoniouthor: Antonio
"""

from PIL import Image
import time 
import numpy as np

print  ("Ddd")
def abreimagen(img):
    
    tiempoin=time.time()
    ruta= ("C:/Users/Antonio/Desktop/ia.trabajo/" + img)
    im= Image.open(open(ruta, 'rb'))
    im.show()
    tiempofin=time.time()
    print ("tardo ", tiempoin - tiempofin , "s")
    

def agrises(img):
    tiempoin=time.time()
    ruta= ("C:/Users/Antonio/Desktop/ia.trabajo/" + img)
    im= Image.open(open(ruta, 'rb'))
    im2= im
    i=0
    while i< im2.size[0]:
        j=0
        while j< im2.size[1]:
            r, g, b = im2.getpixel((i,j))
            g=(r+g+b)/3
            gris= int(g)
            if gris < 65:
                gris=255
            if gris > 140:
                gris=255
            pixel= tuple([gris, gris, gris])
            im2.putpixel((i,j),pixel)
            j+=1
        i+=1
    im2.save("C:/Users/Antonio/Desktop/ia.trabajo/1.bmp")
    im2.show()
    tiempofin=time.time()
    print ("tardo ", tiempofin - tiempoin , "s")

def binarizacion(img,c):
    tiempoin=time.time()
    ruta= (img)
    im= Image.open(open(ruta, 'rb'))
    im2= im
    i=0
    while i< im2.size[0]:
        j=0
        suma=0
        while j< im2.size[1]:
            r, g, b = im2.getpixel((i,j))
            g=(r+g+b)/3
            gris= int(g)
            suma=suma+gris
            j+=1
        prom=suma/im2.size[0]
        #print(prom)
        j=0
        while j< im2.size[1]:
            r, g, b = im2.getpixel((i,j))
            g=(r+g+b)/3
            gris=int(g)
            if gris > (prom*c) or gris <20:
                gris =255
            else: 
                gris=0
            pixel= tuple([gris, gris, gris])
            im2.putpixel((i,j),pixel)
            j+=1
        i+=1
    """im2.save
    im2.show()("C:/Users/Antonio/Desktop/ia.trabajo/2.bmp")
    tiempofin=time.time()
    print ("tardo ", tiempofin - tiempoin , "s")
    print(im2.size[0], ", ", im2.size[1])   """
    return im2
                      
def filtromedia(img,limite):
    ruta= ("C:/Users/Antonio/Desktop/ia.trabajo/" + img)
    im= Image.open(open(ruta, 'rb'))
    """aux=np.zeros((im.shape[0],im.shape[1]),dtype=np.int)"""
    for i in range(1,im.size[0]-1):
        for j in range(1,im.size[1]-1):
            r, g1, b = im.getpixel((i,j))
            r, g2, b =im.getpixel((i+1,j))
            r, g3, b =im.getpixel((i+1,j+1))
            r, g4, b =im.getpixel((i+1,j-1))
            r, g5, b =im.getpixel((i,j-1))
            r, g6, b =im.getpixel((i-1,j-1))
            r, g7, b =im.getpixel((i-1,j))
            r, g8, b =im.getpixel((i-1,j+1))
            r, g9, b =im.getpixel((i,j+1))
            p=(g1+g2+g3+g4+g5+g6+g7+g8+g9)/9
            media=int(p)
            if media > limite:
                im.putpixel((i,j),(255,255,255))
            else:
                im.putpixel((i,j),(0,0,0))
    im.save("C:/Users/Antonio/Desktop/ia.trabajo/3.bmp")
                
            

            
            
            
    
    
    
             
    
    
    
    
    