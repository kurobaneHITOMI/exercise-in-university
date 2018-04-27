#install.packages("Rcpp")
#install.packages("readxl")
#install.packages("rlist")
library(Rcpp)
library(readxl)
library(rlist)
setwd("D:\\课程\\2018\\泰迪杯\\工作数据")

yd1 <- list(
  read.csv(file = "部分数据\\附件1\\YD1设备数据.csv",header = T))
yd2 <- list(
  read.csv(file = "部分数据\\附件1\\YD2设备数据.csv",header = T))
yd3 <- list(
  read.csv(file = "部分数据\\附件1\\YD3设备数据.csv",header = T))
yd4 <- list(
  read.csv(file = "部分数据\\附件1\\YD4设备数据.csv",header = T))
yd5 <- list(
  read.csv(file = "部分数据\\附件1\\YD5设备数据.csv",header = T))
yd6 <- list(
  read.csv(file = "部分数据\\附件1\\YD6设备数据.csv",header = T))
yd7 <- list(
  read.csv(file = "部分数据\\附件1\\YD7设备数据.csv",header = T))
yd8 <- list(
  read.csv(file = "部分数据\\附件1\\YD8设备数据.csv",header = T))
yd9 <- list(
  read.csv(file = "部分数据\\附件1\\YD9设备数据.csv",header = T))
yd10 <- list(
  read.csv(file ="部分数据\\附件1\\YD10设备数据.csv",header = T))
yd11 <- list(
  read.csv(file ="部分数据\\附件1\\YD11设备数据.csv",header = T))

#设备数据分解
device.data <- function(ydlist)
{
  ydlist[[1]] <- ydlist[[1]][,c(2:5)]
  #去除暂态数据
  for(i in as.numeric(names(table(ydlist[[2]]))))
  {
    p <- ydlist[[1]][which(ydlist[[2]]==i),1]
    u <- mean(p)
    c <- sqrt(var(p))
    p <- which(!(p>=(u-2*c)&(p<=(u+2*c))))
    if(length(p)!=0)
    {
      ydlist[[1]] <- ydlist[[1]][-p,]
      ydlist[[2]] <- ydlist[[2]][-p]
    }
  }
  #数据标准化
  ydlist[[1]] <- scale(ydlist[[1]],center=F)
  return(ydlist)
}

#合并数据集
datax <- function(ydl)
{
  a <- NULL
  b <- NULL
  for(i in 1:11)
  {
    a <- rbind(a,ydl[[i]][[1]])
    b <- c(b,ydl[[i]][[2]])
  }
  return(list(a,b))
}

#单一化数据
one.data <- function(ydl)
{
  y <- list(NULL,NULL)
  for (i in as.numeric(names(table(ydl[[2]])))) 
  {
    u <- colMeans(ydl[[1]][which(ydl[[2]]==i),])
    y[[1]] <- rbind(y[[1]],u)
    y[[2]] <- c(y[[2]],i)
  }
  return(y)
}



#功率分解计算
device.power <- function(ydlist)
{
  ydlist[[1]] <- ydlist[[1]][,c(2:6)]
  #去除暂态数据
  for(i in as.numeric(names(table(ydlist[[2]]))))
  {
    p <- ydlist[[1]][which(ydlist[[2]]==i),1]
    u <- mean(p)
    c <- sqrt(var(p))
    p <- which(!(p>=(u-2*c)&(p<=(u+2*c))))
    if(length(p)!=0)
    {
      ydlist[[1]] <- ydlist[[1]][-p,]
      ydlist[[2]] <- ydlist[[2]][-p]
    }
  }
  return(ydlist)
}
#功率数据表
power <- function(ydl)
{
  y <- ydl[[1]]
  y <- y[,1]*0.001*y[,2]*0.1
  p <- list(NULL,NULL)
  for (i in as.numeric(names(table(ydl[[2]])))) 
  {
    u <- mean(y[which(ydl[[2]]==i)])
    p[[1]] <- c(p[[1]],u)
    p[[2]] <- c(p[[2]],i)
  }
  return(p)
}
#功率计算
power.analysis <- function(datam)
{
  r <- datam[,-1]
  p <- matrix(0,nrow = length(datam[,1]),ncol = 11)
  for (i in 1:length(r[,1]))
  {
    for(j in 1:length(r[1,]))
    {
      x <- which(SPECIES[j,]==r[i,j])-1
      x <- ifelse(length(x)==1,x,0)+10*j
      p[i,j] <- ydp[[1]][which(ydp[[2]]==x)]
    }
  }
  return(p)
}


#数据集处理
  yd <- list(yd1,yd2,yd3,yd4,yd5,yd6,yd7,yd8,yd9,yd10,yd11)

  for(i in 1:11)
    yd[[i]] <- c(yd[[i]],list(yd[[i]][[1]][,1]+rep(10*i,length(yd[[i]][[1]][,1]))))

  
  ydp <- lapply(yd,device.power)
  ydp <- datax(ydp)
  ydp <- power(ydp)
  
  yd <- lapply(yd,device.data)
  yd <- datax(yd)
  yd <- one.data(yd)
  


#########################################################################################################################
##########################################################################################################################
         
  
#提取设备编码
matrixTospecies <- function(sequen)
{
  p <- rep(c(4,2,1),11)
  p <- p*sequen
  p <- p%*%(t(rbind(c(1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0),
                    c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1))))
  p <- p + 10*c(1:11)
  return(p)
}
#提取设备状态
getData <- function(x)
{
    x <- which(yd[[2]]==x)
    if(length(x)!=0)
      y <- yd[[1]][x,]
    else
      y <- rep(0,length(yd[[1]][1,]))
  return(y)
}
  
#适应度函数
J <- function(sequen,datax=datax)
{
  sequen <- matrixTospecies(sequen)
  sequen <- lapply(as.list(sequen),getData)
  sequen <- colSums(list.rbind(sequen))
 # sequen <- cor(sequen,datax,method = "pearson") + 1
 # c <- sum(sequen*datax)/sqrt((sum(sequen^2)*sum(datax^2)))
  sequen <- 1000/sum((sequen-datax)^2)
  return(sequen)
}
#交叉
chiasma <- function(generation)
{
  for(i in 1:(m/2))
  {
    j <- round(runif(1,1,32))
    n <- generation[[i]][1:j]
    generation[[i]][1:j] <- generation[[m-i+1]][1:j]
    generation[[m-i+1]][1:j] <- n
  }
  return(generation)
}

#变异
variation <- function(generation)
{
  if(runif(1,0,1) < variation.possibility)
  {
    i <- round(runif(round(runif(1,1,m)),1,m))
    for(j in 1:length(i))
    {
      gene <- generation[[i[j]]]
      n <- round(runif(round(runif(1,1,5)),1,33))
      gene[n] <- 1-gene[n]
      generation[[i[j]]] <- gene
    }
    print("WARNIING,THE GENE VARIATION ACTIVITY")
  }
  return(generation)
}

#######GENETIC ALGORITHM########
GA <- function(yddata)
{
  #初始化个体
  generation <- NULL
  for(i in 1:m)
    generation <- c(generation,list(round(runif(33,0,1))))
  r <- 0
  s <- 0
  pic <- rep(0,g.majority)
  
  for(i in 1:g.majority)
  {
    print(i)
    
    #交叉
    generation <- chiasma(generation)
    #变异
    generation <- variation(generation)
    
    #system.time(selection(generation))
    #选择
    g.j <- as.numeric(lapply(generation,J,datax=yddata))
    pic[i] <- mean(g.j)
    generation.next <- NULL
    s <- sum(g.j)
    g.j <- g.j/s
    g.j <- c(0,cumsum(g.j))
    for(i in 1:m)
    {
      r <- runif(1,0,1)
      generation.next <- c(generation.next,list(generation[[which((g.j>r))[[1]]-1]]))
    }
    generation <- generation.next
    
  }
  plot(pic,type = "l")
  return(generation)
}

SPECIES <- rbind(c("关闭","一档","二档","三档","关闭","关闭","关闭","关闭"),
                 c("关闭","低火","中低火","中火","中高火","高火","关闭","关闭"),
                 c("关闭","打开","关闭","关闭","关闭","关闭","关闭","关闭"),
                 c("关闭","打开","睡眠","重启","关闭","关闭","关闭","关闭"),
                 c("关闭","打开","关闭","关闭","关闭","关闭","关闭","关闭"),
                 c("关闭","打开","关闭","关闭","关闭","关闭","关闭","关闭"),
                 c("关闭","打开","打印","结束","复印","扫描","关闭","关闭"),
                 c("关闭","加热","制冷","保温","关闭","关闭","关闭","关闭"),
                 c("关闭","制冷","除湿","辅热","关闭","关闭","关闭","关闭"),
                 c("关闭","一档热风","一档冷风","二档热风","二档冷风","关闭","关闭","关闭"),
                 c("关闭","打开","关闭","关闭","关闭","关闭","关闭","关闭"))


#变异概率
variation.possibility <- 0.1
#种群数目
m <- 200
#繁殖代数
g.majority <- 200

####################################################################################################
###################################################################################################
device.analysis <- function(ydxlist)
{
  ydxlist[[1]] <- ydxlist[[1]][,c(2:5)]
  ydxlist[[1]] <- scale(ydxlist[[1]],center=F)
  return(ydxlist)
}
NILMD.analysis <- function(ydxlist)
{
  sp <- NULL
  s <- as.character(rep(0,11))
  generation <- apply(ydxlist[[1]],1,GA)
  generation <- lapply(generation,list.rbind)
  for(i in 1:length(generation))
  {
    sequen <- matrixTospecies(round(colMeans(generation[[i]])))
    sequen <- sequen%%10+1
    s <- as.character(rep(0,11))
    for(k in 1:11)
    {
      s[k] <- SPECIES[k,sequen[k]]
    }
    sp <- rbind(sp,s)
  }
  return(sp)
}
####################################################################################################
###################################################################################################
ydx1 <- list(read_excel("A题测试数据\\附件4\\设备组4.xlsx",1))
ydx2 <- list(read_excel("A题测试数据\\附件4\\设备组5.xlsx",1))
ydx3 <- list(read_excel("A题测试数据\\附件4\\设备组6.xlsx",1))
ydx4 <- list(read_excel("A题测试数据\\附件4\\设备组7.xlsx",1))
ydx5 <- list(read_excel("A题测试数据\\附件4\\设备组8.xlsx",1))
ydx1 <- device.analysis(ydx1)
ydx2 <- device.analysis(ydx2)
ydx3 <- device.analysis(ydx3)
ydx4 <- device.analysis(ydx4)
ydx5 <- device.analysis(ydx5)



result.ydx1 <- NILMD.analysis(ydx1)
write.csv(result.ydx1,file = "ydx1.csv")
result.ydx2 <- NILMD.analysis(ydx2)
write.csv(result.ydx2,file = "ydx2.csv")
result.ydx3 <- NILMD.analysis(ydx3)
write.csv(result.ydx3,file = "ydx3.csv")
result.ydx4 <- NILMD.analysis(ydx4)
write.csv(result.ydx4,file = "ydx4.csv")
result.ydx5 <- NILMD.analysis(ydx5)
write.csv(result.ydx5,file = "ydx5.csv")





#result.ydx4.1 <- NILMD.analysis(ydx4.1)
#write.csv(result.ydx4.1,file = "ydx41.csv")
#result.ydx4.2 <- NILMD.analysis(ydx4.2)
#write.csv(result.ydx4.2,file = "ydx42.csv")
#result.ydx4.3 <- NILMD.analysis(ydx4.3)
#write.csv(result.ydx4.3,file = "ydx43.csv")
#result.ydx4.4 <- NILMD.analysis(ydx4.4)
#write.csv(result.ydx4.4,file = "ydx44.csv")
#result.ydx5 <- NILMD.analysis(ydx5)
#write.csv(result.ydx5,file = "ydx5.csv")




#ydp1 <- read.csv(file = "ydx1.csv",header = T)
#ydp2 <- read.csv(file = "ydx2.csv",header = T)
#ydp3 <- read.csv(file = "ydx3.csv",header = T)
#ydp4 <- read.csv(file = "ydx4.csv",header = T)
#ydp5 <- read.csv(file = "ydx5.csv",header = T)

#result.ydp1 <- power.analysis(ydp1)
##write.csv(result.ydp1,file = "ydp1.csv")
#result.ydp2 <- power.analysis(ydp2)
#write.csv(result.ydp2,file = "ydp2.csv")
#result.ydp3 <- power.analysis(ydp3)
#write.csv(result.ydp3,file = "ydp3.csv")
#result.ydp4 <- power.analysis(ydp4)
#write.csv(result.ydp4,file = "ydp4.csv")
#result.ydp5 <- power.analysis(ydp5)
#write.csv(result.ydp5,file = "ydp5.csv")

























