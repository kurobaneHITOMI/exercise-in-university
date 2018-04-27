ld <- cbind(c(0.8293776,1.5344731,-2.2012117,-2.8104603),c(0.02410215,2.16452123,-0.93192121,2.83918785))
iris.data <- as.matrix(subset(iris,select=c(1:4)))
iris.data <- iris.data%*%ld
iris.data <- cbind(iris.data,c(rep(-1,50),rep(1,100)))
colnames(iris.data) <- c("LD1","LD2","Species")

iris.data = iris.data[sample(1:150,150,replace = F),1:3]
iris.train <- iris.data[1:100,]
iris.test <- iris.data[101:150,]

w <- c(0,0)

#train perceptron
for(i in 1:100)
{
  w <- w + iris.train[i,3]*iris.train[i,1:2]
}


#train data
plot(0,xlim = c(-12,10),ylim = c(2,12))
points(iris.train[which(iris.train[,3]==-1),1:2],col="red")
points(iris.train[which(iris.train[,3]==1),1:2],col="blue")

x <- seq(-10,10,by=0.1)
y <- exp(w[1]*x/(-w[2]))
points(x,y,type = "l",col="black")



#test data
s <- c(1:50)
for(i in 1:50)
{
  s[i] <- as.numeric(sign(t(w)%*%iris.test[i,1:2]))
  s[i] <- ifelse(s[i]==iris.test[i,3],1,0)
}
sum(s)/50

points(iris.test[which(iris.test[,3]==-1),1:2],col="orange")
points(iris.test[which(iris.test[,3]==1),1:2],col="purple")


































