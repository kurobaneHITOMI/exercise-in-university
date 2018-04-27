#devide data
data1 <- subset(iris,Species == 'setosa')
data2 <- subset(iris,Species == 'versicolor')
data3 <- subset(iris,Species == 'virginica')

datax1 <- as.matrix(subset(data1,,1:4))
datax2 <- as.matrix(subset(data2,,1:4))
datax3 <- as.matrix(subset(data3,,1:4))
data <- list(datax1,datax2,datax3)

mean1 <- colMeans(datax1)
mean2 <- colMeans(datax2)
mean3 <- colMeans(datax3)

#within-class scatter
sifun <- function(d)
{
  s <- 0
  m <- colMeans(d)
  for(i in 1:40)
    s <- s + (d[i,]-m)%*%t((d[i,]-m))
  return(s)
}
sn <- lapply(data,sifun)

sw <- list(sn[[1]]+sn[[2]],sn[[3]]+sn[[2]],sn[[1]]+sn[[3]])

#between-class scatter
wx <- list(t(sw[[1]])%*%(mean1 - mean2),t(sw[[2]])%*%(mean2 - mean3),t(sw[[3]])%*%(mean1 - mean3))

#trace to lower dimension
tracego <- function(datax,wx)
{
  a <- as.matrix(rep(0,40))
  for(i in 1:40)
    a[i,1] <- datax[i,]%*%wx
  return(a)
}

#trace data
trace11 <- tracego(data[[1]],wx[[1]])
trace12 <- tracego(data[[2]],wx[[1]])
trace22 <- tracego(data[[2]],wx[[2]])
trace23 <- tracego(data[[3]],wx[[2]])
trace31 <- tracego(data[[1]],wx[[3]])
trace33 <- tracego(data[[3]],wx[[3]])

#visualize
plot(trace11,col="red",ylim = c(-200,-500),)
points(trace12,col="orange")
title(main = "1and2")
plot(trace22,col="blue",ylim = c(-400,-900))
points(trace23,col="purple")
title(main = "2and3")
plot(trace31,col="green",ylim = c(-500,-1400))
points(trace33,col="yellow")
title(main = "1and3")


#boudary
y1 <- (mean(trace11)+mean(trace12))/2
y2 <- (mean(trace22)+mean(trace23))/2
y3 <- (mean(trace31)+mean(trace33))/2


#12jugde
jugde12 <- function(x)
{
  a <- t(wx1)%*%x
  if(a>=y1)
    return('setosa')
  else
    return('versicolor')
}
#23jugde
jugde23 <- function(x)
{
  a <- t(wx2)%*%x
  if(a>=y2)
    return('virginica')
  else
    return('versicolor')
}
#13jugde
jugde13 <- function(x)
{
  a <- t(wx3)%*%x
  if(a>=y3)
    return('setosa')
  else
    return('virginica')
}

#classifiction test
testfisher <- function(datax,jugde)
{
  for(i in 41:50)
  {
    a <- jugde(datax[i,])
    print(a)
  }
}


testfisher(datax1,jugde12)
testfisher(datax1,jugde13)

testfisher(datax2,jugde12)
testfisher(datax2,jugde23)

testfisher(datax3,jugde23)
testfisher(datax3,jugde13)

#LDA package
#library(lda)
#lda(Species~Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,iris)
#LD1 <- c(0.8293776,1.5344731,-2.2012117,-2.8104603)
#LD2 <- c(0.02410215,2.16452123,-0.93192121,2.83918785)
trace <- function(datax,wx)
{
  a <- as.matrix(c(1:50))
  b <- as.matrix(c(1:50))
  for(i in 1:50)
    a[i,1] <- (t(LD1)%*%datax[i,])
  for(i in 1:50)
    b[i,1] <- (t(LD2)%*%datax[i,])
  c <- cbind(a,b)
  return(c)
}
#c1 <- trace(datax1)
#c2 <- trace(datax2)
#c3 <- trace(datax3)
#colnames(c1) <- c("LD1","LD2")
#colnames(c2) <- c("LD1","LD2")
#colnames(c3) <- c("LD1","LD2")
#plot(c1,xlim = c(-10,8),ylim = c(4,10),col="red")
#title(main = "LDA????????????")
#points(c2,col="blue")
#points(c3,col="green")