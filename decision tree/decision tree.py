from math import log
import numpy as np
import os
os.chdir("D:\\课程\\2018\\数据挖掘\\5")

import pandas as pd
data_set = pd.read_csv('kohkiloyeh.csv')
data_set = data_set.sample(frac=1).reset_index(drop=True)  
sp = list(data_set.columns)
sp.remove(sp[-1])
dim = data_set.shape
index = range(dim[1]-1)
data_set = np.array(data_set)
label = ['zero','one']
train_data = data_set[1:50,:]
test_data = data_set[50:,:]


#entropy calculation
def ent_cal(p1,p0):
    
    p1 = p1/(p1+p0)
    p0 = p0/(p1+p0)
    if p1==0 or p0==0:
        ent = 0
    else:
        ent = 0 - p0 * log(p0,2) - p1 * log(p1,2)
    
    return(ent)
    


#gain calculation
def gain_cal(var,data):
    
    d = len(pd.Series(data[0]))
    #split data
    var = data[:,var]
    label = data[:,d-1]
    factor = pd.Series(var).value_counts()
    e = 0
    
    #calculate entropy(s)
    p0 = len(np.where(label == 0)[0])/len(label)
    p1 = len(np.where(label == 1)[0])/len(label)
    es = ent_cal(p0,p1)
    
    #calculata cigma[entropy(sv)]
    for i in factor.index:
        s = factor.ix[i]/len(var)
        l = data[np.where(var == i)[0],d-1]
        p0 = len(np.where(l == 0)[0])/len(l)
        p1 = len(np.where(l == 1)[0])/len(l)
        e += s * ent_cal(p1,p0)

    return(es - e)





#check entropy of data list
def data_ent(listdata):
    
    d = 0
    for i in range(len(listdata)):
        label = pd.Series(listdata[i][:,len(listdata[0][0])-1])
        if len(label.value_counts()) != 1:
            a0 = label.value_counts()[0]
            a1 = label.value_counts()[1]
            d = d + a0 * a1
    
    if d <= error:
        return(True)
    else:
        return(False)
        
    




            
#decision tree
def create_tree(datax):
        
    datax = data_set
    e = []
    decision = []
    spe = sp
    
    #first decision
    for i in index:
        e.append(gain_cal(i,datax))#calculate entropy
    n = np.where(e == np.max(e))[0]
    var = pd.Series(list(datax[:,n]))#get variable column
    decision.append([spe[n[0]],var.value_counts().index])#values of variable
    spe.remove(spe[n[0]])#remove already used variable
    data0 = []#initialize
    for k in range(len(var.value_counts().index)):
        s = var.value_counts().index[k][0]
        data0.append(np.delete(datax,n,axis=1)[np.where(var == s)[0],:])
        
    #next decision tree
    while len(data0[0][0]) > 1:
        e = []
        d = []
        data1 = []

        for i in range(len(data0)):
            if len(data0[i]) == 1:#need not to work
                d.append(label[data0[i]])
                data1.append(data0[i])
            else:#it's not already classified
                s = pd.Series(data0[i][:,len(data0[0][0])-1])#label of a leaf
                if len(s.value_counts()) == 1:#it's already classified
                    data0 = np.array(data0)
                    data0[i] = s.value_counts().index[0]
                    data0 = list(data0)
                    d.append(label[list(s.value_counts().index)[0]])
                
                else:
                    if np.abs(s.value_counts()[0] - s.value_counts()[1]) < error:
                        data0 = np.array(data0)
                        data0[i] = s.value_counts().index[0]
                        data0 = list(data0)
                        d.append(label[list(s.value_counts().index)[0]])#values of variable
                        
                    else:                        
                        for n in range(len(data0[0][0])-1):
                            e.append(gain_cal(n,data0[i]))
                        n = np.where(e == np.max(e))[0]#the location of the max grain
                        if len(n) != 1:#more than 1 grains are equal
                            n = [n[0]]                                                             
                        var = pd.Series(list(data0[i][:,n]))
                        d.append(spe[n[0]])#decision  
                        d.append(var.value_counts().index)
                        e = []
                        for k in range(len(var.value_counts().index)):#next layer
                            s = var.value_counts().index[k][0]
                            data1.append(np.delete(data0[i],n,axis=1)[np.where(var == s)[0],:])     
        spe.remove(spe[n[0]])             
        decision.append(d)
        data0 = data1
    #the first one of the leaves
    decision[-1][0] = label[int(round(np.mean(list(data0[0]))))]
    decision[-1].remove(decision[-1][1])
           
    return(decision)        




#parametre initialize
error = 3
d = pd.read_csv('kohkiloyeh.csv')
d = d.sample(frac=1).reset_index(drop=True)  
sp = list(d.columns)
sp.remove(sp[-1])
data_set = np.array(d)





#cut tree
def cut_tree(decision):
    
    l1 = len(decision)
    l2 = 0
    while np.abs(l1-l2) != 1:
        l1 = l2
        c = pd.Series(decision[-1])
        v = c.value_counts().index
        if len(v) == 1:
            del decision[-1]
            decision[-1][0] = v[0]
            del decision[-1][1]
        else:
            break
        l2 = len(decision)
                        
    return(decision)


#classify by decision tree
def classify(vec5):
    
    c = 0
    
    if vec5[1] == 1:
        if vec5[0] == 3:
            c = 1
        if vec5[0] == 2:  
            c = 1
    if vec5[1] == 3:
        c = 0
    if vec5[1] == 2:
        if vec5[2] == 1:
            c = 0
        if vec5[2] == 3:    
            c = 1
    return(c)


       
#test model
def test_tree(data):
     
    s = 0
    for i in data:
        d = list(i)
        c = d[-1]
        del d[-1]
        d = classify(d)
        if d == c:
            s += 1
    print('aggregate:\n',len(data))   
    print('correct:\n',s)
    print('accuracy:\n',s/len(data)) 
    
    
#################################################################################
#RUNNING
d = pd.read_csv('kohkiloyeh.csv')
d = d.sample(frac=1).reset_index(drop=True)  
sp = list(d.columns)
sp.remove(sp[-1])

decision = create_tree(train_data)
decision = cut_tree(decision)

test_tree(test_data)


    