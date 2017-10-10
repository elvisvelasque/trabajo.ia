from PIL import Image, ImageChops
"""from scipy import ndimage"""
import os.path 
import numpy as np
import cv2
import matplotlib.pyplot as plt
import operator
import os

maxancho=0
for letra in os.listdir("alfabeto/"):
	for f in os.listdir("alfabeto/"+letra+"/"):
		print(f)
		im1=Image.open("alfabeto/"+letra+"/"+f)
		ancho,alto=im1.size
		mitad_ancho=int(ancho/2.0)
		mitad_alto=int(alto/2.0)
		pix=im1.load()
		if ancho<53:
			im2=Image.new("L",(52,52))
			im2_pix = im2.load() 
			for i in range(26-mitad_ancho,26+mitad_ancho):
				for j in range(26-mitad_alto,26+mitad_alto):
					if pix[i+mitad_ancho-26,j+mitad_alto-26]>180:
						im2_pix[i,j]=255
			im2.save("alfabetocentrado/"+letra+"/"+f)
			im2.close()
		else:
			os.remove("alfabeto/"+letra+"/"+f)
