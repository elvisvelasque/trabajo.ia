from PIL import Image, ImageChops
"""from scipy import ndimage"""
import os.path 
import numpy as np
import cv2

import matplotlib.pyplot as plt
import operator
import os
import time
import leer

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 500

RESIZED_IMAGE_WIDTH = 40
RESIZED_IMAGE_HEIGHT = 60

###################################################################################################
class ContourWithData():

    # member variables ############################################################################
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False        # much better validity checking would be necessary
        return True




def binarizacion(imagen, umbral):
    ancho, alto = imagen.size
    pix = imagen.load() 
    output = Image.new("L", (ancho, alto))
    out_pix = output.load()
    for i in range(ancho):
        for j in range(alto):
            if pix[i, j] >umbral: out_pix[i, j] = 255
            else: out_pix[i, j] = 0
    return output

def erosion(n):
    image = cv2.imread("a.jpg",0)
    #Crear un kernel de '1' de nxn
    kernel = np.ones((n,n),np.uint8) 
    #Se aplica la transformacion: Erode
    transformacion = cv2.erode(image,kernel,iterations = 1)
    cv2.imwrite("a.jpg" ,transformacion)

def opening(n):
    image = cv2.imread("a.jpg",0)
    #Crear un kernel de '1' de nxn
    kernel = np.ones((n,n),np.uint8) 
    #Se aplica la transformacion: Erode
    transformacion = cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)
    cv2.imwrite("a.jpg" ,transformacion)

def dilation(n):
    imagen = cv2.imread("a.jpg",0)
    #Crear un kernel de '1' de nxn
    kernel = np.ones((n,n),np.uint8) 
    #Se aplica la transformacion: Erode
    transformacion = cv2.dilate(imagen,kernel,iterations = 1)
    cv2.imwrite("a.jpg" ,transformacion)

def closing(n):
    image = cv2.imread("a.jpg",0)
    #Crear un kernel de '1' de nxn
    kernel = np.ones((n,n),np.uint8) 
    #Se aplica la transformacion: Erode
    transformacion = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
    cv2.imwrite("a.jpg" ,transformacion)


def corte(imagen,m,n):
    w1, h1 = imagen.size
    c1=pixels_total_horizontal(imagen)
    for i1 in range(w1):
        if c1[i1]>m:
            T=imagen.crop((i1-1,0,w1,h1))
            break
    w2, h2 = T.size
    c2=pixels_total_horizontal(T)
    for i2 in range(w2):
        if c2[w2-i2-1]>m:
            P=T.crop((0,0,w2-i2,h2))
            break       
    w3, h3 = P.size
    c3=pixels_total_vertical(P)
    for i3 in range(h3):
        if c3[i3]>n:
            Q=P.crop((0,i3-1,w3,h3))
            break
    w4, h4 = Q.size
    c4=pixels_total_vertical(Q)
    for i4 in range(h4):
        if c4[h4-i4-1]>n:
            R=Q.crop((0,0,w4,h4-i4))
            break
    return R

def pixels_total_horizontal(imagen):
    w, h = imagen.size
    pix = imagen.load() 
    histog=w*[0]
    for i in range(w):
        c=0
        for j in range(h):
            if pix[i,j]==255:
                c=c+1
        histog[i]=c
    return histog


def pixels_total_vertical(imagen):
    w, h = imagen.size
    pix = imagen.load() 
    histog=h*[0]
    for j in range(h):
        c=0
        for i in range(w):
            if pix[i,j]==255:
                c=c+1
        histog[j]=c
    return histog

def corte(imagen,m,n):
    w1, h1 = imagen.size
    c1=pixels_total_horizontal(imagen)
    for i1 in range(w1):
        if c1[i1]>m:
            T=imagen.crop((i1-1,0,w1,h1))
            break
    w2, h2 = T.size
    c2=pixels_total_horizontal(T)
    for i2 in range(w2):
        if c2[w2-i2-1]>m:
            P=T.crop((0,0,w2-i2,h2))
            break       
    w3, h3 = P.size
    c3=pixels_total_vertical(P)
    for i3 in range(h3):
        if c3[i3]>n:
            Q=P.crop((0,i3-1,w3,h3))
            break
    w4, h4 = Q.size
    c4=pixels_total_vertical(Q)
    for i4 in range(h4):
        if c4[h4-i4-1]>n:
            R=Q.crop((0,0,w4,h4-i4))
            break
    return R

def conteo_pixels_blanco(imagen):
    cantidad=0
    ancho, alto = imagen.size
    pix = imagen.load()     
    for i in range(ancho):
        for j in range(alto):
            if pix[i,j]==255:
                cantidad=cantidad+1
    return cantidad

def minimo_pixel(imagen):
    c=pixels_total_horizontal(imagen)
    menor=200
    for i in range(len(c)):
        if(c[i]<menor and c[i]!=0):
            menor=c[i]
    return menor

def minimo_pixel_sin_extremos(imagen,a,b):
    c=pixels_total_horizontal(imagen)
    ancho, alto = imagen.size
    menor=200
    for i in range(len(c)):
        if(c[i]<menor and c[i]!=0 and i > ancho*a and i < ancho*b):
            menor=c[i]
    return menor



def seg_minimo_pixel(imagen):
    r=minimo_pixel(imagen)
    c=pixels_total_horizontal(imagen)
    smenor=200
    for i in range(len(c)):
        if(c[i]<smenor and c[i]!=0 and c[i]!=r):
            smenor=c[i]
    return smenor

def thinning():
    imagen = cv2.imread("a.jpg",0)   
    size = np.size(imagen)
    skel = np.zeros(imagen.shape,np.uint8)
    ret,imagen = cv2.threshold(imagen,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    while( not done):
        eroded = cv2.erode(imagen,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(imagen,temp)
        skel = cv2.bitwise_or(skel,temp)
        imagen = eroded.copy()
        zeros = size - cv2.countNonZero(imagen)
        if zeros==size:
            done = True
    cv2.imwrite("a.jpg" ,skel)

def segmentacion(imagen,separador,nsegmentos,lseg,mintotpix):
    his=pixels_total_horizontal(imagen)
    print(his)
    w, h = imagen.size
    letter=False
    foundletter=False
    u=0
    t=0
    p=0
    for i in range(w):
        if letter==True:
            if his[i]<=separador or i==w-1:
                if i== w-1: print (t)
                if t>lseg: 
                    n2=i
                    foundletter=True
                    print("e")
                else:
                    t=t+1
            else:
                t=t+1
        else:
            if his[i]>separador or i==0:
                letter=True
                n1=i
                t=1


        if foundletter==True:
            im = imagen.crop((n1, 0, n2, h))
            print(conteo_pixels_blanco(im))
            if conteo_pixels_blanco(im)>mintotpix:
                u=u+1
                print(u)
                if u==nsegmentos:
                    im = imagen.crop((n1, 0, w, h))
                    im.save(str(nsegmentos)+".jpg")
                    im.close()
                    break
                elif u<nsegmentos:
                    leer.borrarauxexp(str(u)+"jpg")
                    im.save(str(u)+".jpg")
                    im.close()
                    p=n1
            foundletter=False
            letter=False
    
    if u<nsegmentos:
        im1 = imagen.crop((p, 0, w, h))
        im1.save(str(u)+".jpg")
        im1.close()
            
    return u


def segmentacion_thin(imagen1,imagen2,separador,nsegmentos,lseg):
    leer.borraraux2()
    his=pixels_total_horizontal(imagen2)
    print(his)
    w, h = imagen2.size
    letter=False
    foundletter=False
    u=0
    t=0
    p=0
    for i in range(w):
        if letter==True:
            if his[i]<=separador or i==w-1:
                if t>lseg: 
                    n2=i
                    foundletter=True
                else:
                    t=t+1
            else:
                t=t+1
        else:
            if his[i]>separador or i==0:
                letter=True
                n1=i
                t=1

        if foundletter==True:
            im = imagen1.crop((n1, 0, n2, h))
            if conteo_pixels_blanco(im)>9:
                u=u+1
                if  u==nsegmentos:
                    im1 = imagen1.crop((n1, 0, w, h))
                    im1.save(str(u)+".jpg")
                    im1.close()
                    break
                elif u<nsegmentos:
                    im.save(str(u)+".jpg")
                    p=n1
                    im.close()
            foundletter=False
            letter=False
    if u<nsegmentos:
        im1 = imagen1.crop((p, 0, w, h))
        im1.save(str(u)+".jpg")
        im1.close()
    print(u)

    return u





def quitar_mancha(imagen):
    ancho, alto = imagen.size
    pix = imagen.load() 
    output = Image.new("L", (ancho, alto))
    out_pix = output.load()
    
    for i in range(ancho):
        fin=1
        for j in range(alto):
            if pix[i,j]==0 and fin:
                out_pix[i,j]=255
            else:
                fin=0
                out_pix[i,j]=pix[i,j]

    return output
    
def filtromoda(imagen):
    ancho, alto = imagen.size
    pix = imagen.load() 
    output = Image.new("L", (ancho, alto))
    out_pix = output.load()
    for i in range(1,ancho-1):
        for j in range(1,alto-1):
            
            if pix[i,j] ==0:
                out_pix[i,j]=pix[i,j]
            else:
                c=0
                for x in range(i-1,i+1,1):
                    for y in range(j-1,j+1,1):
                        if pix[x,y]==0:
                            c=1+c
                
                            c=1+c
                if c>5:
                    out_pix[i,j]=0

                else:
                    out_pix[i,j]=255
                    if c>4 :
                        print(i, " " , j)
                        print(c)
                    
    return output


def quitar_linea(imagen,L):
    anchu, altu = imagen.size
    out = imagen.load()
    outps = Image.new("L", (anchu, altu))
    out_ps = outps.load()
    pix = L.load() 
    for n in range(anchu):
        for m in range(altu):            
            if(out[n, m]==0):
                if (pix[n, m] == 0):
                        out_ps[n, m]=255
                        if m != altu-1:
                            out_ps[n,m+1]=255
                        if m !=  0:
                            out_ps[n,m-1]=255
                else:
                    if out_ps[n, m]!=255:
                        out_ps[n, m]=out[n, m]
            else:
                if out_ps[n, m]!=255:
                    out_ps[n, m]=out[n, m]
    return outps


def segmentar(minpix,nseg,Lminseg,k,mintotpix):
    leer.borraraux()
    c=leer.total_arch("C:/Users/Antonio/Desktop/ia.trabajo/segmentada",k)
    print(c)
    if c<5:
        for i in range(c):     
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            m=segmentacion(im1,minpix,nseg,Lminseg,mintotpix)
            im1.close()
            print(m,n,c)
            if m>1  :            
                for r in range(c,i+1,-1):
                    print(r)
                    os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))
                    
                os.remove("segmentada/"+str(i+1)+"."+str(k))
                for s in range(m): 
                    os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
                break
    leer.borraraux()

def segmentarforzado(k):
    c=leer.total_arch("C:/Users/Antonio/Desktop/ia.trabajo/segmentada",k)
    print(c)
    Lmax=0
    p=0
    if c<5:
        for i in range(c):
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            ancho, alt=im1.size
            im1.close()
            if ancho>Lmax:
                Lmax=ancho
                p=i+1
        im1=Image.open("segmentada/"+str(p)+"."+str(k))
        his=pixels_total_horizontal(im1)
        minpix=100
        for i in range(int(round(Lmax/3.0,0))+1,int(2.0*round(Lmax/3.0,0))):
            if his[i]<minpix:
                minpix=his[i]
        print(minpix,Lmax,p,"sd")
        im1.close()
           
            
        im1=Image.open("segmentada/"+str(p)+"."+str(k))
        m=segmentacion(im1,minpix,2,round(Lmax/3),0)
        im1.close()
        print(m,n,c)
        if m==2  :            
            for r in range(c,p,-1):
                print(r)
                os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+1)+"."+str(k))
                   
            os.remove("segmentada/"+str(p)+"."+str(k))
            for s in range(m): 
                os.rename(str(s+1)+".jpg", "segmentada/"+str(p+s)+"."+str(k))
        
    leer.borraraux()        



def segmentarthin(minpix,nseg,Lminseg,k):
    c=leer.total_arch("segmentada/",k)
    print(c)
    if c<5:
        for i in range(c):
            leer.borraraux()
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            im1.save("a.jpg")
            dilation(2)
            M=Image.open("a.jpg")
            N=binarizacion(M, 90)
            M.close()
            leer.borrarauxexp("a.jpg")
            N.save("a.jpg")
            thinning()
            dilation(2)
            N.close()
            P=Image.open("a.jpg")
            Q=binarizacion(P, 90)
            m=segmentacion_thin(im1,Q,minpix,nseg,Lminseg)
            P.close()
            Q.close()
            im1.close()
            if m>1:            
                for r in range(c,i+1,-1):
                    print(r)
                    os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))
                    
                os.remove("segmentada/"+str(i+1)+"."+str(k))
                for s in range(m): 
                     os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
                break 
    leer.borraraux2()

"""              
ruta=("C:/Users/Antonio/Desktop/ia.trabajo/prueba.jpg")
im= Image.open(open(ruta, 'rb'))
im2=im.convert("L")
im2.save("C:/Users/Antonio/Desktop/ia.trabajo/gris.jpg")
L=binarizacion(im2,40) #linea
L.save("C:/Users/Antonio/Desktop/ia.trabajo/linea.jpg")
w, h = im2.size
pix = im2.load() 
im3 = Image.new("L", (w, h))
im3_pix = im3.load()
for i in range(w):
    sum=0
    for k in range(h):
        sum=sum+pix[i,k]
    p=sum/h
    p=int(p)
    for j in range(h):
        if pix[i, j] >= p: im3_pix[i, j] = 255
        else: im3_pix[i, j] = 0 
    im3.save("C:/Users/Antonio/Desktop/ia.trabajo/binarizada.jpg")

im4=quitar_mancha(im3)
im4.save("C:/Users/Antonio/Desktop/ia.trabajo/sinmancha.jpg")
imsl=quitar_linea(im4,L)
imsl.show()
imsl.save("C:/Users/Antonio/Desktop/ia.trabajo/sinlinea.jpg")
im5=ImageChops.invert(imsl)
im5.save("C:/Users/Antonio/Desktop/ia.trabajo/invertida.jpg")
im5.show()
im6=corte(im5,0,0)
im6.save("C:/Users/Antonio/Desktop/ia.trabajo/cortada.jpg")
im6.save("C:/Users/Antonio/Desktop/ia.trabajo/a.jpg")

thinning()
dilation(2)
H=Image.open("a.jpg")
Z=binarizacion(H, 90)
Z.save("thin.jpg")
im6.save("C:/Users/Antonio/Desktop/ia.trabajo/cortada.jpg")
n=segmentacion_thin(im6,Z,0,5,50)

"""
##########################################################################################################################################################
##########################################################################################################################################################  
##########################################################################################################################################################

for k in leer.listdir_recurd([],'C:/Users/Antonio/Desktop/ia.trabajo/img','C:/Users/Antonio/Desktop/ia.trabajo/img', []):
    print(k)
    leer.borraraux()
    I = Image.open("img/"+k)

    #convertir a gris
    G = I.convert("L")
    G.save("gris/"+k)
    #binarizar imagen para que se vea solo la linea
    LN=binarizacion(G, 40) 
    LN.save("linea/"+k)

    #binarizar imagen para quitar el color de fondo de la imagen
    w, h = G.size
    pix = G.load() 
    output = Image.new("L", (w, h))
    out_pix = output.load()
    for i in range(w):
        sum=0
        for a in range(h):
            sum=sum+pix[i,a]
        p=sum/h
        p=int(p)
        for j in range(h):
            if pix[i, j] >= p: out_pix[i, j] = 255
            else: out_pix[i, j] = 0	
    output.save("binarizada/"+k)
    
     #quitar mancha
    A=quitar_mancha(output)
    A.save("sinmancha/"+k)

    #quitar linea
    C=quitar_linea(A,LN)
    C.save("sinlinea/"+k)


    #invertir colores de la imagen
    out = ImageChops.invert(C)
    out.save("invertida/"+k)
    
    #corte
    Ct=corte(out,2,2)
    Ct.save("cortada/"+k)
    Ct.save("a.jpg")
    dilation(2)
    M=Image.open("a.jpg")
    N=binarizacion(M, 90)
    N.save("a.jpg")
    thinning()
    dilation(2)
    N.close()
    M.close()
    P=Image.open("a.jpg")
    Q=binarizacion(P, 90)
    n=segmentacion_thin(Ct,Q,0,5,30)
    P.close()    
    print(n)
    for i in range(n):
        if os.path.exists(str(i+1)+".jpg"):
            L=Image.open(str(i+1)+".jpg")
            L.save("segmentada/"+str(i+1)+"."+str(k))
            L.close()

    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/"+str(i+1)+"."+str(k)):
            R=Image.open("segmentada/"+str(i+1)+"."+str(k))
            w, h = R.size
            R.close()  
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
             
            break
    
    print(k)

    if n<5 and n>0:
        print(m,n,c)        
        for i in range(n):
            leer.borraraux()
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            m=segmentacion(im1,0,6-n,27,90)
            im1.close()
            print(m,n,c)
        if m>1:            
            for r in range(c,i+1,-1):
                print(r)
                os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))

            os.remove("segmentada/"+str(i+1)+"."+str(k))
            for s in range(m): 
                os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
            


    segmentar(0,6-n,23,k,80)
    segmentar(1,6-c,23,k,85)
    segmentar(0,6-n,20,k,85)
    segmentarthin(0,6-c,22,k)

    segmentar(1,6-c,22,k,85)
    segmentarthin(1,6-c,25,k)
    segmentarthin(2,5-c,20,k)
    segmentar(2,6-c,25,k,85)
    segmentarthin(2,6-c,20,k)
    segmentar(2,6-c,20,k,70)
    segmentar(3,6-c,20,k,80)
    segmentarthin(3,6-c,20,k)
    segmentar(3,6-c,20,k,70)
    segmentar(5,6-c,20,k,70)
    segmentar(6,6-c,20,k,70)
    segmentarforzado(k)

    for i in range(5):
        letra=k[i]
        os.rename("segmentada/"+str(i+1)+"."+str(k), "alfabeto/"+str(letra)+"/"+str(letra)+"."+str(i)+"."+str(k))

    os.remove("img/"+str(k))




"""
    n=0
    m=0
              
    for i in range(5):
        if os.path.exists("segmentada/"+str(i+1)+"."+str(k)):
            R=Image.open("segmentada/"+str(i+1)+"."+str(k))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        F=Image.open("segmentada/"+str(c)+"."+str(k))
        F.save("a.jpg")
        dilation(2)
        M=Image.open("a.jpg")
   N=binarizacion(M, 90)
        N.save("a.jpg")
        thinning()
        dilation(2)
        P=Image.open("a.jpg")
        Q=binarizacion(P, 90)
       
        m=segmentacion_thin(F,Q,3,6-n,69)
        print(m)
       
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))
                  


    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        im1=Image.open("segmentada/%d-%d.jpg" %(k,c))
        m=segmentacion(im1,2,6-n,65)
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))

    

    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        im1=Image.open("segmentada/%d-%d.jpg" %(k,c))
        m=segmentacion(im1,3,6-n,65)
        if m>1:
            
          
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))


    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        im1=Image.open("segmentada/%d-%d.jpg" %(k,c))
        m=segmentacion(im1,4,6-n,65)
        if m>1:
            
          
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))

    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        im1=Image.open("segmentada/%d-%d.jpg" %(k,c))
        m=segmentacion(im1,minimo_pixel_sin_extremos(im1,0.3,0.7),6-n,70)
        if m>1:
            
          
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))

          
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        im1=Image.open("segmentada/%d-%d.jpg" %(k,c))
        m=segmentacion(im1,minimo_pixel_sin_extremos(im1,0.4,0.6),6-n,70)
        if m>1:
            
          
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))

             
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        F=Image.open("segmentada/%d-%d.jpg" %(k,c))
        F.save("a.jpg")
        dilation(2)
        M=Image.open("a.jpg")
        N=binarizacion(M, 90)
        N.save("a.jpg")
        thinning()
        dilation(2)
        P=Image.open("a.jpg")
        Q=binarizacion(P, 90)
        
        m=segmentacion_thin(F,Q,5,6-n,60)
       
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))
                  
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        F=Image.open("segmentada/%d-%d.jpg" %(k,c))
        F.save("a.jpg")
        dilation(2)
        M=Image.open("a.jpg")
        N=binarizacion(M, 90)
        N.save("a.jpg")
        thinning()
        dilation(2)
        P=Image.open("a.jpg")
        Q=binarizacion(P, 90)
        
        m=segmentacion_thin(F,Q,7,6-n,60)
       
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))
       
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        F=Image.open("segmentada/%d-%d.jpg" %(k,c))
        F.save("a.jpg")
        dilation(2)
        M=Image.open("a.jpg")
        N=binarizacion(M, 90)
        N.save("a.jpg")
        thinning()
        dilation(2)
        P=Image.open("a.jpg")
        Q=binarizacion(P, 90)
        
        m=segmentacion_thin(F,Q,8,6-n,50)
       
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))
       
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
            w, h = R.size
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        F=Image.open("segmentada/%d-%d.jpg" %(k,c))
        F.save("a.jpg")
        dilation(2)
        M=Image.open("a.jpg")
        N=binarizacion(M, 90)
        N.save("a.jpg")
        thinning()
        dilation(2)
        P=Image.open("a.jpg")
        Q=binarizacion(P, 90)
        
        m=segmentacion_thin(F,Q,12,6-n,50)
       
        if m>1:
            
            for i in range(n):
                if n-i==c:
                    for j in range(m):
                        F=Image.open("%d.jpg" % (j+1))
                        F.save("segmentada/%d-%d.jpg" %(k,(c+j)))
                elif n-i>c:
                    os.rename( "segmentada/%d-%d.jpg" %(k,n-i), "segmentada/%d-%d.jpg" %(k,n-i+m-1))


    n=0
    for i in range(5):
        if os.path.exists("segmentada/%d-%d.jpg" %(k,(i+1))):
            n=n+1
        else:
            break

    if n<5:

        g=g+1
    FinalString = ""
    for i in range(n):
        R=Image.open("segmentada/%d-%d.jpg" %(k,(i+1)))
        Q=corte(R,0,0)
        T=Q.resize((40,60), Image.BICUBIC)
        T.save("segmentada/%d-%d.jpg" %(k,(i+1)))
        
                
    #reconocimiento
        allContoursWithData = []                # declare empty lists,
        validContoursWithData = []              # we will fill these shortly

        try:
            npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
        except:
            print ("error, unable to open classifications.txt, exiting program\n")
            
        # end try

        try:
            npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
        except:
            print ("error, unable to open flattened_images.txt, exiting program\n")
            
        # end try

        npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

        kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object

        kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

        As=Image.open("segmentada/%d-%d.jpg" %(k,i+1))
        As.save("e.jpg")
        imgTestingNumbers = cv2.imread("e.jpg")          # read in testing numbers image

        if imgTestingNumbers is None:                           # if image was not read successfully
            print ("error: image not read from file \n\n")        # print error message to std out
                                                         # and exit function (which exits program)
        # end if

        imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)       # get grayscale image
        imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
        imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                          255,                                  # make pixels that pass the threshold full white
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                          cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                          11,                                   # size of a pixel neighborhood used to calculate threshold value
                                          2)                                    # constant subtracted from the mean or weighted mean

        imgThreshCopy = imgThresh.copy()        # make a copy of the thresh image, this in necessary b/c findContours modifies the image

        imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points

        for npaContour in npaContours:                             # for each contour
            contourWithData = ContourWithData()                                             # instantiate a contour with data object
            contourWithData.npaContour = npaContour                                         # assign contour to contour with data
            contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
            contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
            contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
            allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data
        # end for

        for contourWithData in allContoursWithData:                 # for all contours
            if contourWithData.checkIfContourIsValid():             # check if valid
                validContoursWithData.append(contourWithData)       # if so, append to valid contour list
            # end if
        # end for

        validContoursWithData.sort(key = operator.attrgetter("intRectX"))         # sort contours from left to right

        strFinalString = ""         # declare final string, this will have the final number sequence by the end of the program
        strCurrentChar = ""

        for contourWithData in validContoursWithData:            # for each contour
                                                # draw a green rect around the current char
            cv2.rectangle(imgTestingNumbers,                                        # draw rectangle on original testing image
                          (0, 0),     # upper left corner
                          (40, 60),      # lower right corner
                          (0, 255, 0),              # green
                          2)                        # thickness

            imgROI = imgThresh[0 : 60,     # crop char out of threshold image
                               0 : 40]

            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consistent for recognition and storage

            npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

            npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

            retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)     # call KNN function find_nearest

            strCurrentChar = str(chr(int(npaResults[0][0]))) # get character from results
            

        strFinalString = strFinalString + strCurrentChar            # append current char to full string
    # end for
        FinalString = FinalString + strFinalString
    print ("%d " %k,FinalString,"\n")                  # show the full string

    cv2.destroyAllWindows()             # remove windows from memory
"""