#normalize data
knormalize <- function(x)
{
  min <- min(x)  
  max <- max(x)  
  for(i in 1:length(x))  
    x[i]<-(x[i]-min)/(max-min)  
  return(x)  
}

irisdata <- apply(as.matrix(iris[,1:4]),2,knormalize)

#calculate distance
distance <- function(data)
{
  dis <- rep(0,length(irisdata[,1]))
  for(i in 1:length(irisdata[,1]))
  dis[i] <- sqrt(sum((data - irisdata[i,1:4])^2))
  return(dis)
}


#k neighbor classifiction
kneighbor <- function(k,i)
{ 
  k <- k+1
  a <- 0
  dis <- distance(irisdata[i,])#?distance
  disx <- as.data.frame(cbind(as.matrix(dis),as.matrix(iris$Species)))
  colnames(disx) <- c("distance","species")
  
  if(k == 1)
    element <- disx[order(disx$distance),][2,]$species#k=1 select the nearest
  else
    element <- disx[order(disx$distance),][2:k+1,]$species#select k nearest
  element <- as.data.frame(table(element))#statistic
  element <- subset(element,Freq == max(Freq))
  
  if(element$element == iris[i,5])
    a <- 1
  print(element)
  print(iris[i,5])
  return(a)
}

#test
verify <- function()
{ 
  k <- scan("")
  a <- as.matrix(round(runif(50,1,150)))
  b <- 0
  for(i in 1:50)
  {
    c <- kneighbor(k,a[i,])
    if(c ==1)
      b <- b+1
  }
  print(b/50)
}
verify()