#loading data
library(softmaxreg)
path="D:\\课程\\2017\\模式识别\\usps"
x= load_image_file(paste(path,'train-images.idx3-ubyte', sep=""))
y= load_label_file(paste(path,'train-labels.idx1-ubyte', sep=""))
xTest= load_image_file(paste(path,'t10k-images.idx3-ubyte',sep=""))
yTest= load_label_file(paste(path,'t10k-labels.idx1-ubyte', sep=""))



#print iamge in train data
showmedigit_train <- function(k)
{ 
  digit <- matrix(data = 0,nrow = 28,ncol = 28)
  for(i in 1:28)
  {
    digit[i,] <- as.vector(x[k,][(1+28*(i-1)):(28*i)])
  }
  print(digit)
  show_digit(x[k,])
  return(y[k])
}
#print iamge in test data
showmedigit_test <- function(k)
{ 
  digit <- matrix(data = 0,nrow = 28,ncol = 28)
  for(i in 1:28)
  {
    digit[i,] <- as.vector(xTest[k,][(1+28*(i-1)):(28*i)])
  }
  print(digit)
  show_digit(xTest[k,])
  return(yTest[k])
}



#normalize data
knormalize1 <- function(x)
{
  min <- min(x)  
  max <- max(x)  
  for(i in 1:length(x))
    x[i]<-(x[i]-min)/(max-min)
  return(x)
}
knormalize2 <- function()
{
  data <- x
  for(i in 1: length(y))
  {
    data[i,] <- knormalize1(x[i,])
  }
  return(data)
}
usps_train_data <- knormalize2()


#E distance between sample and train data
distance <- function(data)
{
  dis <- rep(0,length(y))
  data <- knormalize1(data)
  data <- sapply(data,rep,length(y))
  dis <- sqrt(rowSums((data-usps_train_data)^2))
  return(dis)
}



#K neighbor
kneighbor <- function(k,i)
{
  a <- 0
  dis <- distance(xTest[i,])
  dis <- as.data.frame(cbind(as.numeric(dis),y))
  colnames(dis) <- c("distance","species")

  element <- dis[order(dis$distance),][1:k,]$species
  element <- as.data.frame(table(element))
  element <- subset(element,Freq == max(Freq))
  
  showmedigit_test(i)
  
  if(element$element == yTest[i])
  {
    a <- 1
    print("TRUE")
  }
  else print("FLASE")
  print(element)
  print(yTest[i])
  return(a)
}

verify <- function()
{
  print("give me the quality of k")
  k <- scan("")
  print("give me the quality of i")
  i <- scan("")
  kneighbor(k,i)
}
verify()