#data
data1 <- cbind(as.matrix(subset(iris,select=c(1:4))),c(1:150))
colnames(data1)[5] <- "Species"


#give the nearest center
dis_g <- function(x)
{
  da <- sapply(x[1:4],rep,length(g[,1]))
  dis <- rowSums((da - g)^2)
  return(which(rank(dis)==1))
}


#k means
k_means <- function(data1)
{
  ep <- 0
  while(ep != e)
  {
    ep <- ep + 1
    #label
    data1[,5] <- apply(data1,1,dis_g)

    #devide data
    s1 <- as.matrix(subset(as.data.frame(data1),Species == 1))[,1:4]
    s2 <- as.matrix(subset(as.data.frame(data1),Species == 2))[,1:4]
    s3 <- as.matrix(subset(as.data.frame(data1),Species == 3))[,1:4]
    
    #iterate clustering centre
    gx <- rbind(colMeans(s1),colMeans(s2),colMeans(s3))
  }
  return(gx)
}

#parametre
majority <- 3
e <- 20

######################     ??  ??    ####################
g <- cbind(runif(majority,4,8),runif(majority,2,4),runif(majority,3,5),runif(majority,1,2))
g <- k_means(data1)

