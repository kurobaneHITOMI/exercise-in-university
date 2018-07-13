import os
os.chdir("D:\\课程\\2018\\生产实习\\image data")
import cv2
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import random
from tqdm import tqdm
import ggplot as gp
import pandas as pd
T = np.array([128,64,32,16,8,4,2,0]).reshape(8,1)

#parametre
variation_possibility = 0.1
mating_possibility = 1
generation_size = 50
iteration_times = 200
C = 3


#display image
def display_image(img):
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#plot picture
def ggplot_img(xt):
    xt = pd.DataFrame({'n':range(len(xt)),'xt':xt})
    p = gp.ggplot(gp.aes(x='n',y='xt'),data = xt) + gp.geom_line(color='black')
    print(p)

##############################################################################################
'''
Genetic algorithm FCM based on histogram analysis
'''

'''
FCM
'''

#calculate cluster center
def center_calculation(gene):
    g = np.array(gene).reshape(C,8)
    g = np.dot(g,T)
    return(g)


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
        

#put class by center
def put_class(center):
    dim = center.shape[0]
    species = np.arange(256)
    d = distance(center)
    dmin = np.min(d,axis=0)
    for i in range(dim):
        species[np.where(d[i] == dmin)[0]] = i
    return(species)


#optimize funciton
def J(gene,hist):
    center = center_calculation(gene)
    d = distance(center)
    member_mat = membership_calculation(center)
    h = np.tile(hist,(C,1))
    return(1/np.sum(d * member_mat * h))

'''
Genetic algorithm
'''

#Initialize generation
def generation_initialization():
    generation = []
    for i in range(generation_size):
        generation.append(np.random.randint(0,2,8*C))
    generation = np.array(generation)
    return(generation)


#variation
def variation(generation):
    if random.uniform(0,1) < variation_possibility:
        dim = generation.shape
        i = random.randrange(0,generation_size)
        g = generation[i,:]
        try:
            j = random.randrange(0,dim[1])
            g[j] = 1 - g[j]
            generation[i,:] = g
        finally:
            return(generation)
    return(generation)


#creat new generation
def mating(generation):
    if random.uniform(0,1) < mating_possibility:
        dim = generation.shape
        for i in range(int(generation_size/2)):
            n = random.randrange(0,dim[1])
            generation[i,0:n],generation[dim[0]-i-1,0:n] = generation[dim[0]-i-1,0:n],generation[i,0:n]
        return(generation)


#selection
def selection(generation,hist):
    dim = generation.shape
    j = np.apply_along_axis(J,1,generation,hist)
    generation_next = []
    n1 = []
    
    j1 = sorted(j)[0:int(generation_size/2)]
    for i in range(len(j1)):
        n1.append(np.where(j == j1[i])[0][0])#worse gene
    n2 = list(set(range(generation_size)) - set(n1))#better gene
    
    #definitly select the better gene
    generation_next = generation[n2,:]    
    #randomly select the worse gene
    g = generation[sorted(n1),:]
    j1 = j[sorted(n1)]
    j1 = np.cumsum(j1)/np.sum(j1)
    for _ in range(int(generation_size/2)):
        i = random.uniform(0,1)
        generation_next = np.concatenate((generation_next,g[np.where(j1 > i)[0][0],:].reshape(1,dim[1])),axis=0)
    return(generation_next)
        
        
###### GENETIC ALGORITHM #######
def GENETIC_ALGORITHM_FCM(hist):
    generation = generation_initialization()
    j = []
    for _ in tqdm(range(iteration_times)):
        generation = selection(generation,hist)
        generation = variation(generation)
        generation = mating(generation)
        j.append(1/np.max(np.apply_along_axis(J,1,generation,hist)))
        
    a = np.apply_along_axis(J,1,generation,hist)
    a = np.where(a == sorted(a)[0])[0][0]
    ggplot_img(j)
    return(generation[a,:],j)
        
##############################################################################################
'''
processing after cluster
'''

#rebuild image
def rebuild_image(img,hist,clu):
    n = center_calculation(clu)
    n = put_class(n)
    img0 = np.zeros(img.shape,dtype='uint8')
    for i in range(C):
        species = np.where(n==i)[0]
        if len(species) != 0:
            for j in range(species.min(),species.max()+1):
                img0[np.where(img == j)] = i
    img0 = img0/(C-1)*255
    img0 = img0.astype('uint8')
    return(img0)


##############################################################################################
'''
image divide
'''
#image data
img = cv2.imread("1.jpg")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
display_image(img)
#histogram
hist = np.histogram(img.ravel(),256,[0,256])[0]
#cluster
clu,j = GENETIC_ALGORITHM_FCM(hist)
#rebuild image
img1 = rebuild_image(img,hist,clu)
display_image(img1)

##############################################################################################