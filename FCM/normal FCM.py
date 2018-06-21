import numpy as np
import os
os.chdir("D:\\课程\\2017\\模式识别\\FCM")
import random
from tqdm import tqdm
from sklearn import preprocessing

#distance calculation
def distance(datax,center):
    #initialize
    k = center.shape[0]
    dim = datax.shape
    #rebuild data and center
    datax = np.tile(datax,(k,1,1))
    c = []
    for i in range(k):
        c.append(np.tile(center[i],dim))
    c = np.array(c)
    d = np.apply_along_axis(sum,2,(datax - c)**2)
    return(d)
    
    
#membership calculation
def membership_calculation(datax,center):
    k = center.shape[0]
    d = distance(datax,center)
    d = d / np.tile(np.apply_along_axis(sum,0,d),(k,1))
    return(d)   
    
    
#center reculculation
def new_center(member_mat,center):
    dim = center.shape
    for i in range(dim[0]):
        center[i] = np.sum(member_mat[i] * center[i]) / np.sum(member_mat[i])
    return(center)
    
    
#classification
def put_class(datax,center):
    dim = center.shape
    species = np.arange(datax.shape[0])
    d = distance(datax,center)
    dmin = np.min(d,axis=0)
    for i in range(dim[0]):
        species[np.where(d[i] == dmin)[0]] = i
    return(species)  
    
    
#FCM
def FCM_clster(datax,k):
    
    #initialize
    dim = datax.shape
    datax = preprocessing.scale(datax,axis=0)
    center = []
    for i in range(k):
        center.append(datax[random.randint(0,dim[0]),:])
    center = np.array(center)
    
    for i in tqdm(range(20)):
        member_mat = membership_calculation(datax,center)
        center = new_center(member_mat,center)

    s = put_class(datax,center)
    return(s)