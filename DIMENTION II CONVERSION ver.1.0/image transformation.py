import os
os.chdir("D:\\课程\\2018\\图像处理与计算机视觉\\大作业")
import cv2
import numpy as np
from photoshopy import pspy as ps
import  dlib
np.seterr(divide='ignore', invalid='ignore')
import random
from tqdm import tqdm
import skimage.measure as skm

##############################################################################################
'''
get image outline
'''

#get outline
def sketch_outline(img , min_filter , sharpen , blur_n , bilateral_r , bias):    

    img0 = np.zeros(img.shape,dtype='uint8')
    img0 += img
    
    #split
    img1 = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
    img2 = img1    
        
    #outline
    img2 = ps.mixed_model.invertion(img1)
    img2 = ps.normal_fliter.min_filter(img2,min_filter)
    img2 = ps.mixed_model.Linear_burn(img1,img2)
    
    
    #sharpen
    if sharpen != 0:
        img2 = ps.normal_fliter.sharpen_filter(img2,sharpen)   
    #bilateral
    if bilateral_r != 0:
        img2 = cv2.bilateralFilter(img2,bilateral_r,np.var(img1)/100,4)  
    #blur
    if blur_n != 0:
        img2 = cv2.medianBlur(img2,blur_n)        
    #bias
    if bias != 0:
        img2 = ps.normal_fliter.thresholding(img2,bias)
    print('sketch outline OVER')
    return(img2)


##############################################################################################
'''
cluster
FCM based on histogram analysis
'''

#distance calculation
def distance(center):
    #initialize
    k = center.shape[0]
    dim = 256
    hist = np.arange(0,256)
    #rebuild data and center
    hist = np.tile(hist,(k,1))
    c = []
    for i in range(k):
        c.append(np.tile(center[i],dim))
    c = np.array(c)
    d = np.sqrt((hist - c)**2)
    return(d)
    
    
#membership calculation
def membership_calculation(center):
    k = center.shape[0]
    d = distance(center)
    d = d / np.tile(np.apply_along_axis(sum,0,d),(k,1))
    return(d)
    
    
#center reculculation
def new_center(hist,member_mat,center):
    dim = center.shape
    for i in range(dim[0]):
        center[i] = np.sum(member_mat[i] * hist * center[i]) / np.sum(member_mat[i] * hist)
    return(center)
    
    
#classify histogram
def put_class(center):
    dim = center.shape[0]
    species = np.arange(256)
    d = distance(center)
    dmin = np.min(d,axis=0)
    for i in range(dim):
        species[np.where(d[i] == dmin)[0]] = i
    return(species)
    

#optimize funciton
def J(member_mat,center):
    d = distance(center)
    d = d * member_mat
    return(np.sum(d))


#FCM
def FCM_clster(hist,c):
    
    #initialize
    center = []
    center.append(random.randint(200,256))
    for i in range(c-1):
        center.append(random.randint(0,200))
    center = np.array(center).reshape(c,1)
    
    for i in range(10):
        member_mat = membership_calculation(center)
        center = new_center(hist,member_mat,center)

    s = put_class(center)
    j = J(member_mat,center)
    return(s,j)
    

#cluster and selection
def optimize_FCM_cluster(hist,k,n):
    label = []
    optimize_j = []
    for i in tqdm(range(n)):
        s,j = FCM_clster(hist,k)
        label.append(s)
        optimize_j.append(j)
    s = label[np.where(optimize_j == np.max(optimize_j))[0][0]]
    print('sky cluster OVER')
    return(s)


##############################################################################################
'''
processing after cluster
'''

#rebuild image
def rebuild_image(img1,hist,s,k):
    issky = np.where(s==0)[0]
    isnotsky = np.where(s!=0)[0]
    for j in range(isnotsky.min(),isnotsky.max()+1):
        img1[np.where(img1 == j)] = 0
    for j in range(issky.min(),issky.max()+1):
        img1[np.where(img1 == j)] = 1
    return(img1)

##############################################################################################
'''
sky recognition and replace
'''

#sky material
def sky_modern():    
    s1 = cv2.imread("sky//sunrise.jpg")
    s2 = cv2.imread("sky//afternoon.jpg")
    s3 = cv2.imread("sky//evening.jpg")
    m1 = np.mean(cv2.cvtColor(s1,cv2.COLOR_BGR2HSV)[:,:,2])
    m2 = np.mean(cv2.cvtColor(s2,cv2.COLOR_BGR2HSV)[:,:,2])
    m3 = np.mean(cv2.cvtColor(s3,cv2.COLOR_BGR2HSV)[:,:,2])
    sky = {'sunrise':s1,'afternoon':s2,'evening':s3,'b1':m1,'b2':m2,'b3':m3}
    return(sky)


#connected graph in 01 image for selecting real sky area
def divide_sky(img,alpha):
    img1 = np.zeros(img.shape,dtype='uint8')
    img1 += img
    dim = img.shape
    img2 = skm.label(img1,connectivity = 2)        
    for i in tqdm(range(1,np.max(img2)+1)):
        location = np.where(img2 == i)
        if len(img2[location]) / (dim[0]*dim[1]) < alpha:
            img1[location] = 0
    print('divide sky area OVER')
    return(img1)


#candidate sky area by FCM cluster and select
def sky_recognition(img,alpha):
    img0 = np.zeros(img.shape,dtype='uint8')
    img0 += img
    img0 = cv2.medianBlur(img0,3)
    img1 = img0[:,:,0]
    hist = np.histogram(img1.ravel(),256,[0,256])[0]
    s = optimize_FCM_cluster(hist,2,50)
    sky = rebuild_image(img1,hist,s,2)
    sky = divide_sky(sky,alpha)
    return(sky)


#replace image sky
def sky_replace(img,sky,mode,sky_img):
    m = ['sunrise','afternoon','evening'][mode]
    img0 = np.zeros(img.shape,dtype='uint8')
    img0 += img
    dim1 = img.shape
    dim2 = sky[m].shape
    i = random.randint(0,dim2[0]-dim1[0])
    j = random.randint(0,dim2[1]-dim1[1])
    img1 = sky[m][i:i+dim1[0],j:j+dim1[1],:]
    for n in range(3):
        img0[:,:,n] = cv2.equalizeHist(img0[:,:,n])
        img0[:,:,n] = img1[:,:,n] * sky_img + img0[:,:,n] * (1-sky_img)
    return(img0)


##############################################################################################
'''
image transformantion
'''

def image_transfer(img,mode):
    dim = img.shape
    #oil painting
    img1 = ps.normal_fliter.oil_painting(img,6)
    
    #adjust brightness
    i = ['b1','b2','b3'][mode]
    i = sky[i]
    i -= np.mean(cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)[:,:,2])
    img1 = ps.normal_fliter.contrast_and_brightness(img1,1,i)
    
    #sky divide
    img2 = sky_recognition(img,alpha)
    #sky replace
    if np.sum(img2) > dim[0]*dim[1]*0.01:
        img1 = sky_replace(img1,sky,mode,img2)
    
    #outline
    img0 = sketch_outline(img1 , min_filter , sharpen , blur_n , bilateral_r , bias)
    img0 = 255 - (255-cv2.blur(img0,(5,5))) * (255-img0)
    img0 = cv2.bilateralFilter(img0,bilateral_r,np.var(img0)/100,4)
    img0 = img0.astype('float16')
    img0 = img0 / 255
    #outline cover
    img1 = img1.astype('float16')
    for i in range(3):
        img1[:,:,i] = img1[:,:,i] * img0
    img1 = img1.astype('uint8')
    
    #after process
    img1 = cv2.bilateralFilter(img1,bilateral_r,np.var(img1)/100,4)
    'img1 = cv2.blur(img1,(3,3))'
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    img1 = ps.normal_fliter.contrast_and_brightness(img1,1.3,16)
    print('image transformantion OVER')
    return(img1)

##############################################################################################
'''
parametre
'''
sky = sky_modern()
min_filter = 1
sharpen = 1
blur_n = 0
bilateral_r = 5
bias = 32
alpha = 0.1
mode = 1

##############################################################################################
'''
test
'''
img = cv2.imread("IMG_20161107_123314.jpg")
img = cv2.imread("IMG_20170724_115727.jpg")
img = cv2.imread("IMG_20170727_172856.jpg")
img = cv2.imread("IMG_20161002_173350.jpg")
img = cv2.imread("IMG_20151216_150955.jpg")
img = cv2.imread("IMG_20170131_101134.jpg")
img = cv2.imread("IMG_20161107_123315.jpg")

img1 = image_transfer(img,mode)
win = dlib.image_window()
win.set_image(img1)