#patametre
cross_k = 40

from PIL import Image  
import pandas as pd
import numpy as np
import os
os.chdir("D:\\课程\\2018\\数据挖掘\\6")
np.set_printoptions(precision = 5)

#load data
face_data = np.zeros((1,10305))
for i in range(1,21):
    for j in range(1,11):
        data = np.array(Image.open("att_faces\\s{0}\\{1}.jpg".format(i,j)).convert("L").getdata(),dtype='float')
        data = np.append(data,i)
        face_data = np.row_stack((face_data,data))
face_data = np.delete(face_data,0,0)
face_label = face_data[:,-1]
face_data = np.delete(face_data,-1,1)


#data analysis
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn import svm

#PCA
face_data = PCA(n_components=0.9).fit_transform(face_data)
#dimension
dim = face_data.shape
#nomalize
face_data = preprocessing.scale(face_data)



##############################################################################
face_data = np.column_stack((face_data,face_label))
face_data = pd.DataFrame(face_data).sample(frac=1)
face_data = np.array(face_data)

#test data
test_data = face_data[0:cross_k,:]
test_label = test_data[0:cross_k,-1]
test_data = np.delete(test_data,-1,1)

#device data
def device_data(data):
    
    data = pd.DataFrame(data).sample(frac=1)
    data = np.array(data)
    
    validate_data = data[cross_k:(2*cross_k),:]
    validate_data = np.delete(validate_data,-1,1)
    validate_label = data[cross_k:(2*cross_k),-1]
    
    train_data = data[(2*cross_k):,:]
    train_data = np.delete(train_data,-1,1)
    train_label = data[(2*cross_k):,-1]
    
    
    return(train_data,train_label,validate_data,validate_label)
    
    
#estimate model
def accuracy_estimate(model,face_data):
    
    acc = []
    for i in range(interation_n):
        train_data,train_label,validate_data,validate_label = device_data(face_data)
        model.fit(train_data,train_label)#train
        p = model.predict(validate_data)#predict
        acc.append(  sum(p == validate_label) / len(p)  )#accuracy
        
    return( [('%.5f' % np.mean(acc)) , ('%.5f' % np.var(acc))] )
        
##############################################################################    
'''  
C = 1.0,                 松弛变量         Slack Variable                  √
kernel = 'rbf',          使用核           kernel                          √
degree = 3,              多项式次数       degree of poly                   √
gamma = 1/n_features     核系数          kernel parametre                 √
coef0 = 0.0,             核常数项        constant for poly and sigmoid     √
shrinking = True,        已知支撑向量     if sv are known
probability = False,     使用概率估计     use probability
tol = 0.001,             停机误差        error to stop iteration
max_iter = -1            最大迭代次数     -1 means infinity
'''           

#####################

# rbf kernel
#c
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=i,
                kernel='rbf', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#gamma
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=3,
                kernel='rbf', 
                gamma=i*0.0005)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#estimate rbf
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=3,
                kernel='rbf', 
                gamma=0.0025)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)

#####################

# sigmoid kernel
#c
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=i,
                degree = 3,
                coef0 = 0.0,
                kernel='sigmoid', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#degree
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = i,
                coef0 = 0.0,
                kernel='sigmoid', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#coef0
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = 6,
                coef0 = i*0.001,
                kernel='sigmoid', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#gamma
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = 6,
                coef0 = 0.008,
                kernel='sigmoid', 
                gamma=i*0.001)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#estimate sigmoid
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = 6,
                coef0 = 0.008,
                kernel='sigmoid', 
                gamma=0.013)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)

#####################

#poly kernel
#degree
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=i,
                degree = 3,
                coef0 = 0.0,
                kernel='poly', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#degree
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=5,
                degree = i,
                coef0 = 0.0,
                kernel='poly', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#coef0
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=5,
                degree = 6,
                coef0 = 4 + i,
                kernel='poly', 
                gamma='auto')
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#gamma
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = 6,
                coef0 = 17,
                kernel='poly', 
                gamma=i*0.001)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T)
#estimate poly
accuracy = []
for i in range(1,20):
    model = svm.SVC(
                C=2,
                degree = 6,
                coef0 = 17,
                kernel='poly', 
                gamma=0.005)
    accuracy.append(accuracy_estimate(model,face_data))
print(pd.DataFrame(accuracy).T) 

#####################

#probability
interation_n = 200
#sigmoid
model = svm.SVC(
        C=2,
        degree = 6,
        coef0 = 0.008,
        kernel='sigmoid',
        probability = True,
        gamma=0.013)
print(accuracy_estimate(model,face_data))
#poly
model = svm.SVC(
        C=2,
        degree = 6,
        coef0 = 17,
        kernel='poly', 
        probability = True,
        gamma=0.005)
print(accuracy_estimate(model,face_data))


#####################

#tol
#sigmoid
model = svm.SVC(
        C=2,
        degree = 6,
        coef0 = 0.008,
        kernel='sigmoid',
        tol = 0.00001,
        gamma=0.013)
print(accuracy_estimate(model,face_data))
#poly
model = svm.SVC(
        C=2,
        degree = 6,
        coef0 = 17,
        kernel='poly', 
        tol = 0.00001,
        gamma=0.005)
print(accuracy_estimate(model,face_data))

##############################################################################

#model test
train_data = face_data[cross_k:,:]
train_data = np.delete(train_data,-1,1)
train_label = face_data[cross_k:,-1]

model = svm.SVC(C=2,degree = 6,coef0 = 0.008,kernel='sigmoid',gamma=0.013)
model.fit(train_data,train_label)
p = model.predict(test_data)
sum(p == test_label) / len(p)

model = svm.SVC(C=2,degree = 6,coef0 = 17,kernel='poly',gamma=0.005)   
model.fit(train_data,train_label)
p = model.predict(test_data)
sum(p == test_label) / len(p)