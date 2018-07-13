import os
os.chdir("D:\\课程\\2018\\生产实习\\image data")
import cv2
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import pywt
import random
from tqdm import tqdm
import skimage.measure as skm


#read gray image
def read_image_data(f1,f2,f3):
    img1 = cv2.imread(f1)
    img2 = cv2.imread(f2)
    img3 = cv2.imread(f3)
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    img3 = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
    return(img1,img2,img3)
        
    
#display image
def display_image(img):
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

##############################################################################################    
'''
image fusion
'''
#mean ratio image
def mean_ration_img(img1,img2,window):
    img1 = cv2.blur(img1,(window,window))
    img2 = cv2.blur(img2,(window,window))
    img1,img2 = img1/img2 , img2/img1
    Xm = np.zeros(img1.shape)
    Xm[np.where(img1 >= img2)] = img2[np.where(img1 >= img2)]
    Xm[np.where(img1 < img2)] = img1[np.where(img1 < img2)]
    Xm = 1 - Xm
    return(Xm)


#log ration image
def log_ration_img(img1,img2):
    i1 = img1.astype('int')
    i2 = img2.astype('int')
    return(np.abs(np.log(i1+1) - np.log(i2+1)))


#fusion rule for lh hl hh
def fustion_rule(w1,w2,window):
    d1 = w1**2
    d2 = w2**2
    e1 = cv2.filter2D(d1,-1,np.ones((window,window)))
    e2 = cv2.filter2D(d2,-1,np.ones((window,window)))
    d = np.zeros(w1.shape)
    d[np.where(e1 >= e2)] = w2[np.where(e1 >= e2)]
    d[np.where(e1 < e2)] = w1[np.where(e1 < e2)]
    return(np.array(d))


#enhance image
def enhance(img,window,alpha):
    f = np.ones((window,window))
    n = int((window - 1)/2)
    f[n,n] = 0
    n = window**2 - 1
    img1 = cv2.filter2D(img,-1,f)
    img2 = 1/(1+alpha)*(img + (alpha/n)*img1)
    return(img2)
    
def SNR(img1,img2):
    return(10*np.log10(np.sum(img1**2)/np.sum((img1-img2)**2)))
    
def enhance_rate_determination(img,window):
    s = []
    for i in range(1,10):
        img1 = img
        img2 = enhance(img1,window,i/10)
        s.append(SNR(img1,img2))
    return((np.where(s == np.max(s))[0][0]+1) / 10)


#image fusion
def image_fusion(img1,img2,window):    
    p1 = mean_ration_img(img1,img2,window)
    p2 = log_ration_img(img1,img2)    
    #wavelet    
    w1 = list(pywt.wavedec2(p1,'haar',level=2))
    w2 = list(pywt.wavedec2(p2,'haar',level=2))
    #fusion
    w_fusion = []
    w_fusion.append((w1[0]+w2[0])/2)#LL
    w = []
    for n in range(len(w1)-1):        
        for i in range(3):#lh,hk,hh
            w.append(fustion_rule(w1[n+1][i],w2[n+1][i],window))
        w_fusion.append(w)
        w = []
    #rebiuld
    img = pywt.waverec2(w_fusion,'haar')    
    return(img)


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
def FCM_clster(hist):
    
    #initialize
    i = np.round(sum(hist * np.arange(0,256)) / sum(hist))
    center = []
    center.append(random.randint(0,i))
    center.append(random.randint(i,256))
    center = np.array(center).reshape(2,1)
    
    for i in range(10):
        member_mat = membership_calculation(center)
        center = new_center(hist,member_mat,center)

    s = put_class(center)
    j = J(member_mat,center)
    return(s,j)
    

##############################################################################################
'''
processing after cluster
'''

#rebuild image
def rebuild_image(img,hist,s,k):
    for i in range(k):
        species = np.where(s==i)[0]
        for j in range(species.min(),species.max()+1):
            img[np.where(img == j)] = i
    return(img)
    
##############################################################################################
'''
change detection
'''
#change detection
def change_detection(img1,img2,window):
    
    #image fuion and enhance
    img = image_fusion(img1,img2,window)
    a = enhance_rate_determination(img,window)
    img = enhance(img,window,a)       
    #normalize
    img = np.round((img - img.min()) / (img.max() - img.min()) * 255)
    #bilateralFilter
    img = img.astype('uint8')
    img = cv2.bilateralFilter(img,3,np.sqrt(np.var(img))/2,np.sqrt(np.var(img)))
    #histogram
    hist = np.histogram(img.ravel(),256,[0,256])[0]
    #cluster and selection
    label = []
    optimize_j = []
    for i in tqdm(range(50)):
        s,j = FCM_clster(hist)
        label.append(s)
        optimize_j.append(j)
    s = label[np.where(optimize_j == np.max(optimize_j))[0][0]]
    #rebuild image
    s = rebuild_image(img,hist,s,2)
    return(s)


#divide big object
def divide_object(img,alpha):
    img1 = np.zeros(img.shape,dtype='uint8')
    img1 += img
    dim = img.shape
    img2 = skm.label(img1,connectivity = 2)        
    for i in range(1,np.max(img2)+1):
        location = np.where(img2 == i)
        if len(img2[location]) / (dim[0]*dim[1]) < alpha:
            img1[location] = 0
    return(img1)
    
##############################################################################################
'''
break in detection
'''

#judge break in or not
def break_judge(change_img,forbidden_area):
    
    #ajust image size
    i = [min(change_img.shape[0],forbidden_area.shape[0]),min(change_img.shape[1],forbidden_area.shape[1])]
    change_img = change_img[0:i[0],0:i[1]]
    forbidden_area = forbidden_area[0:i[0],0:i[1]]
    detect_img = change_img & forbidden_area
    
    #judgement
    warning = 0
    i = change_img.shape[0] * change_img.shape[1]
    i = np.sum(forbidden_area)**2 / i
    if np.sum(detect_img) / i > (1-alarm_level)/10:
        warning = 1
        print('GET OUT THERE!')
    else:
        print('NO PROBLEM')
    return(warning)
    
    
#break in detection    
def break_detection(img1,img2,img3):
    change_img = change_detection(img1,img2,window)
    change_img = divide_object(change_img,alpha).astype('int')    
    forbidden_area = (img3 / 255).astype('int')        
    a = break_judge(change_img,forbidden_area)
    dim = img2.shape
    l = [int((dim[0]-insert_size[0])/2),int((dim[1]-insert_size[1])/2)]
    if a == 1:
        img2[l[0]:l[0]+insert_size[0],l[1]:l[1]+insert_size[1]] *= warning
    else:
        img2[l[0]:l[0]+insert_size[0],l[1]:l[1]+insert_size[1]] *= safe
    display_image(img2)
    return(a)

        
##############################################################################################
'''
run
'''

#parametre
window = 3
alpha = 1e-4
alarm_level = 5

warning = cv2.imread('warning.jpg')
warning = cv2.cvtColor(warning,cv2.COLOR_BGR2GRAY)
warning = (warning/255).astype('uint8')
safe = cv2.imread('safe.jpg')
safe = cv2.cvtColor(safe,cv2.COLOR_BGR2GRAY)
safe = (safe/255).astype('uint8')
insert_size = safe.shape

#test
img1,img2,img3 = read_image_data("1a.jpg","1b.jpg","1c.jpg")
img1,img2,img3 = read_image_data("2a.jpg","2b.jpg","2c.jpg")
img1,img2,img3 = read_image_data("3a.jpg","3b.jpg","3c.jpg")
    
w = break_detection(img1,img2,img3)



##############################################################################################