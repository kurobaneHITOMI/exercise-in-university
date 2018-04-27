library(ggplot2)
library(R.matlab)

setwd("D:\\课程\\2018\\数据挖掘\\4")

s8 <- as.data.frame(readMat('square4.mat')$b)[,1:2]

# mean shift
Mean.Shift <- function(datax)
{
  
  center <- datax[round(runif(n,1,length(datax[,1]))),][,1:length(datax[1,])]
  e <- 1
  
  while(e > ep)
  {
    for(i in 1:length(center[,1]))
    {
      d <- center
      #label
      c <- sapply(center[i,],rep,length(datax[,1]))
      distance <- rowSums((datax[,1:length(datax[1,])] - c)^2)
      a <- which(distance<r)
      #cener moving
      if(sum(a) != 0)
        center[i,] <- colMeans(datax[a,])
    }
    e <- sqrt(sum((d-center)^2))
  }
  #normalize
  for(i in 1:(length(center[,1])-1))
  {
    for(j in (i+1):length(center[,1]))
    {
      d <- sqrt(sum((center[i,]-center[j,])^2))
      if(d < dis)
        center[j,] <- center[i,]
    }
  }
  
  center <- center[which(!duplicated(center)),]
  return(center)
}

#label
ms.species <- function(center,datax)
{
  datax <- cbind(datax,rep(0,length(datax[,1])))
  for(i in 1:length(datax[,1]))
  {
    d <- sapply(datax[i,],rep,length(center[,1]))[,1:(length(datax[1,])-1)]
    d <- rowSums((d-center)^2)
    datax[i,length(datax[1,])] <- which(rank(d)==1)
  }
  return(datax)
}

#cluster
ms.cluster <- function(datax)
{
  center <- Mean.Shift(datax)
  datax <- ms.species(center,datax)
  return(datax)
}

#parametre
n <- 10
r <- 1
dis <- 6
ep <- 1e-08


#################################################################
c <- Mean.Shift(s8)
d <- ms.species(c,s8)


g8 <- ggplot(data = d,aes(x=d[,1],y=d[,2])) + 
  geom_point(colour = d[,3]+1) + 
  labs(title="square4 - mean shift cluster",x="x", y = "y")
g8
