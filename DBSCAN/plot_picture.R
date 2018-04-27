library(ggplot2)
library(R.matlab)

setwd("D:\\课程\\2018\\数据挖掘\\4")

s1 <- as.data.frame(readMat('2d4c.mat')$a)
write.csv(s1,file = '2d4c.csv',row.names = FALSE)
s2 <- as.data.frame(readMat('long.mat')$long1)
write.csv(s2,file = 'long.csv',row.names = FALSE)
s3 <- as.data.frame(readMat('moon.mat')$a)
write.csv(s3,file = 'moon.csv',row.names = FALSE)
s4 <- as.data.frame(readMat('sizes5.mat')$sizes5)
write.csv(s4,file = 'sizes5.csv',row.names = FALSE)
s5 <- as.data.frame(readMat('smile.mat')$smile)
write.csv(s5,file = 'smile.csv',row.names = FALSE)
s6 <- as.data.frame(readMat('spiral.mat')$spiral)
write.csv(s6,file = 'spiral.csv',row.names = FALSE)
s7 <- as.data.frame(readMat('square1.mat')$square1)
write.csv(s7,file = 'square1.csv',row.names = FALSE)
s8 <- as.data.frame(readMat('square4.mat')$b)
write.csv(s8,file = 'square4.csv',row.names = FALSE)


g1 <- ggplot(data = s1,aes(x=s1[,1],y=s1[,2])) + 
  geom_point(colour = s1[,3]+1) + 
  labs(title="2d4c",x="x", y = "y")
g1


g2 <- ggplot(data = s2,aes(x=s2[,1],y=s2[,2])) + 
  geom_point(colour = s2[,3]+1) + 
  labs(title="long",x="x", y = "y")
g2


g3 <- ggplot(data = s3,aes(x=s3[,1],y=s3[,2])) + 
  geom_point(colour = s3[,3]+1) + 
  labs(title="moon",x="x", y = "y")
g3


g4 <- ggplot(data = s4,aes(x=s4[,1],y=s4[,2])) + 
  geom_point(colour = s4[,3]+1) + 
  labs(title="sizes5",x="x", y = "y")
g4


g5 <- ggplot(data = s5,aes(x=s5[,1],y=s5[,2])) + 
  geom_point(colour = s5[,3]+1) + 
  labs(title="smile",x="x", y = "y")
g5


g6 <- ggplot(data = s6,aes(x=s6[,1],y=s6[,2])) + 
  geom_point(colour = s6[,3]+1) + 
  labs(title="spiral",x="x", y = "y")
g6


g7 <- ggplot(data = s7,aes(x=s7[,1],y=s7[,2])) + 
  geom_point(colour = s7[,3]+1) + 
  labs(title="square1",x="x", y = "y")
g7


g8 <- ggplot(data = s8,aes(x=s8[,1],y=s8[,2])) + 
  geom_point(colour = s8[,3]+1) + 
  labs(title="square4",x="x", y = "y")
g8

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################

r1 <- as.data.frame(read.csv('2d4c_cluster.csv'))
r2 <- as.data.frame(read.csv('long_cluster.csv'))
r3 <- as.data.frame(read.csv('moon_cluster.csv'))
r4 <- as.data.frame(read.csv('sizes5_cluster.csv'))
r5 <- as.data.frame(read.csv('smile_cluster.csv'))
r6 <- as.data.frame(read.csv('spiral_cluster.csv'))
r7 <- as.data.frame(read.csv('square1_cluster.csv'))
r8 <- as.data.frame(read.csv('square4_cluster.csv'))


#ggplot start
g1 <- ggplot(data = r1,aes(x=r1[,1],y=r1[,2])) + 
  geom_point(aes(colour = factor(r1[,3]))) + 
  labs(title="2d4c",x="x", y = "y")
g1


g2 <- ggplot(data = r2,aes(x=r2[,1],y=r2[,2])) + 
  geom_point(aes(colour = factor(r2[,3]))) + 
  labs(title="long",x="x", y = "y")
g2


g3 <- ggplot(data = r3,aes(x=r3[,1],y=r3[,2])) + 
  geom_point(aes(colour = factor(r3[,3]))) + 
  labs(title="moon",x="x", y = "y")
g3


g4 <- ggplot(data = r4,aes(x=r4[,1],y=r4[,2])) + 
  geom_point(aes(colour = factor(r4[,3]))) + 
  labs(title="sizes5",x="x", y = "y")
g4


g5 <- ggplot(data = r5,aes(x=r5[,1],y=r5[,2])) + 
  geom_point(aes(colour = factor(r5[,3]))) + 
  labs(title="smile",x="x", y = "y")
g5


g6 <- ggplot(data = r6,aes(x=r6[,1],y=r6[,2])) + 
  geom_point(aes(colour = factor(r6[,3]))) + 
  labs(title="spiral",x="x", y = "y")
g6


g7 <- ggplot(data = r7,aes(x=r7[,1],y=r7[,2])) + 
  geom_point(aes(colour = factor(r7[,3]))) + 
  labs(title="square1",x="x", y = "y")
g7


g8 <- ggplot(data = r8,aes(x=r8[,1],y=r8[,2])) + 
  geom_point(aes(colour = factor(r8[,3]))) + 
  labs(title="square4",x="x", y = "y")
g8