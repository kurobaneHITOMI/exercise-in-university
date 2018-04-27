import os
os.chdir("D:\\课程\\2018\\数据挖掘\\4")

import math
import numpy
numpy.set_printoptions(suppress=True)

import mat4py
data2d4c = numpy.array(mat4py.loadmat('2d4c.mat')['a'])
datalong = numpy.array(mat4py.loadmat('long.mat')['long1'])
datamoon = numpy.array(mat4py.loadmat('moon.mat')['a'])
datasizes5 = numpy.array(mat4py.loadmat('sizes5.mat')['sizes5'])
datasmile = numpy.array(mat4py.loadmat('smile.mat')['smile'])
dataspiral = numpy.array(mat4py.loadmat('spiral.mat')['spiral'])
datasquare1 = numpy.array(mat4py.loadmat('square1.mat')['square1'])
datasquare4 = numpy.array(mat4py.loadmat('square4.mat')['b'])

##########################################################################
##########################################################################



#parametre
r = 0.2
minpts = 5



#data in some area
def get_neighbours(p,data):
    
    l,d = data.shape
    n = []
    
    dis = numpy.apply_along_axis(sum,1,(numpy.tile(data[p],[l,1])-data)**2)
    r1 = numpy.tile(r,[l])
    dis = list(dis**0.5 - r1)
    for i in range(l):
        if dis[i] < 0:
            n.append(i)
    n.remove(p)
    
    return(n)
    
    
    
    
#expand area
def expandcluster(p,data,c,species):

    #haven't been visited
    if species[p] == 99:
        visited = []
        #scan
        for i in range(len(species)):
            if species[i] != 99:
                visited.append(i)
        #expand
        n = get_neighbours(p,data)
        visited.append(p)
        if len(n) < minpts:
            species[p] = 0 #noise
        else:
            species[p] = c
            while len(n) != 0:
                i = get_neighbours(n[0],data)
                if len(i) < minpts:
                    if species[n[0]] == 99:
                        species[n[0]] = 0 #noise
                        visited.append(n[0])
                        n = set(n + i)
                        n = list(n - set(visited))
                else:
                    if species[n[0]] == 99:
                        species[n[0]] = c
                        visited.append(n[0])
                        n = set(n + i)
                        n = list(n - set(visited))                   
        
    return(species)
        
    
    
    

#dbscan cluster
def dbscan(data_set):
    
    #dimension
    l,d = data_set.shape
    d -= 1
    #label（0 for noise）
    c = 0
    p = 0

    species = numpy.tile(99,[l])
    data = data_set[0:l,0:d]
    
    while p < len(data):
        c += 1
        species = expandcluster(p,data,c,species)
        p += 1
        
    return(species)



# data fusion
def data_cluster(data_set,species):

    
    l,d = data_set.shape
    d -= 1

    data = numpy.column_stack((data_set[0:l,0:d],species))

    return(data)
            


#output

r = 0.5
minpts = 5
s1 = dbscan(data2d4c)
numpy.savetxt('2d4c_cluster.csv', data_cluster(data2d4c,s1), delimiter = ',')



r = 0.2
minpts = 5
s2 = dbscan(datalong)
numpy.savetxt('long_cluster.csv', data_cluster(datalong,s2), delimiter = ',')



r = 0.2
minpts = 5
s3 = dbscan(datamoon)
numpy.savetxt('moon_cluster.csv', data_cluster(datamoon,s3), delimiter = ',')



r = 1
minpts = 3
s4 = dbscan(datasizes5)
numpy.savetxt('sizes5_cluster.csv', data_cluster(datasizes5,s4), delimiter = ',')



r = 0.05
minpts = 3
s5 = dbscan(datasmile)
numpy.savetxt('smile_cluster.csv', data_cluster(datasmile,s5), delimiter = ',')



r = 1
minpts = 5
s6 = dbscan(dataspiral)
numpy.savetxt('spiral_cluster.csv', data_cluster(dataspiral,s6), delimiter = ',')



r = 1
minpts = 5
s7 = dbscan(datasquare1)
numpy.savetxt('square1_cluster.csv', data_cluster(datasquare1,s7), delimiter = ',')



r = 1
minpts = 3
s8 = dbscan(datasquare4)
numpy.savetxt('square4_cluster.csv', data_cluster(datasquare4,s8), delimiter = ',')




