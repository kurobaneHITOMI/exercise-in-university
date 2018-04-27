ex1data1 <- read.csv(file = "D:\\?γ?\\2017\\???Ż?\\?ϻ???ҵ\\ex1data1.txt",header = F)
colnames(ex1data1) <- c("x","y")
z=lm(ex1data1[,2]~ex1data1[,1],data = ex1data1)
plot(ex1data1,col='red',pch=10)
lines(ex1data1[,1],fitted(z))



#data
ex2data2 <- as.matrix(read.csv(file = "D:\\?γ?\\2017\\???Ż?\\?ϻ???ҵ\\ex1data2.txt",header = F))
y <- subset(ex2data2,,3)/10000
x <- cbind(rep(1,length(y)),subset(ex2data2,,1:2))
#parametre
m <- length(y)
a <- 0.0000001
#initialize
theta <- as.vector(c(0,0,0))
maxn <- 20
j <- rep(0,maxn)

gd <- function()
{
  for(i in 1:maxn)
  {
    theta <- theta - (a/m)*t(x)%*%((x%*%theta) - y)
    j[i] <- (1/(2*m))*sum(((x%*%theta) - y)^2)
  }
  print(theta)
  return(j)
}
j <- gd()
n <- c(1:maxn)
plot(n,j,col="blue",type = "l")


#image
library(rgl)
theta <- c(9.067246e-06,1.653821e-02,2.720592e-05)
pred <- matrix(0,nrow = 47,ncol = 47)
for(i in 1:47)
{
  for(j in 1:47)
  {
    pred[i,j] <- theta[1]+theta[2]*x[i,2]+theta[3]*x[j,3]
  }
}
plot3d(x[,2],x[,3],y, col="red",type="s", size=0.5, lit=FALSE,xlab = "The size of the house",ylab="The number of bedrooms",zlab = "Price")
surface3d(x[,2],x[,3],pred,alpha=0.5,front="line",back="lines")