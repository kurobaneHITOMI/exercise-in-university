sonar <- read.csv(file = "D:\\?γ?\\2017\\ģʽʶ??\\sonar\\sonar.txt",header = F)
#library(rlist)
#parametre
variation.possibility <- 0.1
m <- 200
g.majority <- 500




#fitness function
J <- function(sequen)
{
  #rebuild data
  sequen <- sapply(sequen,rep,length(sonar[,1]))
  datax <- sequen*sonar[,1:60]
  datax <- cbind(datax,sonar[,61])
  #devide data
  data1 <- subset(datax,datax[,61] == 'R')
  data2 <- subset(datax,datax[,61] == 'M')
  data1 <- as.matrix(subset(data1,,1:60))
  data2 <- as.matrix(subset(data2,,1:60))
  mean1 <- apply(data1,2,mean)
  mean2 <- apply(data2,2,mean)

  s1 <- apply(data1,2,sd)
  s1 <- t(s1)%*%s1
  s2 <- apply(data2,2,sd)
  s2 <- t(s2)%*%s2
  sw <- s1 + s2
  sb <- t(mean1 - mean2)%*%(mean1 - mean2)
  return(1000*sb/sw)
}

#generation select
selection <- function(g)
{
  r <- 0
  s <- 0
  g.j <- as.numeric(lapply(g,J))
  generation.next <- NULL

  s <- sum(g.j)
  g.j <- g.j/s
  gj2 <- rep(0,m+1)

  for(i in 1:m)
    gj2[i+1] <- sum(g.j[1:i])

  for(i in 1:m)
  {
    r <- runif(1,0,1)
    generation.next <- c(generation.next,list(g[[which((gj2>r))[[1]]-1]]))
  }
  return(generation.next)
}

#chiasma
chiasma <- function(generation)
{
  for(i in 1:(m/2))
  {
    j <- round(runif(1,1,length(sonar)-1))
    n <- generation[[i]][1:j]
    generation[[i]][1:j] <- generation[[m-i+1]][1:j]
    generation[[m-i+1]][1:j] <- n
  }
  return(generation)
}

#variation
variation <- function(generation)
{
  if(runif(1,0,1) < variation.possibility)
  {
    #random life to variate
    i <- round(runif(1,1,m))
    gene <- generation[[i]]
    #random gene to variate
    n <- round(runif(1,1,60))
    gene[n] <- 1-gene[n]
    #rebuild
    generation[[i]] <- gene
    print("WARNIING,THE GENE VARIATION ACTIVITY")
  }
  return(generation)
}


#######GENETIC ALGORITHM########
GA <- function(generation)
{
  pic <- rep(0,g.majority)
  for(i in 1:g.majority)
  {
    print(i)
    #system.time(selection(generation))
    generation <- selection(generation)
    #system.time(chiasma(generation))
    generation <- chiasma(generation)

    generation <- variation(generation)

    pic[i] <- max(as.numeric(lapply(generation,J)))
  }
  plot(pic,type = "l")
  return(generation)
}

#initialize
generation <- NULL
for(i in 1:m)
  generation <- c(generation,list(round(runif(60,0,1))))

generation <- GA(generation)
generation[[1]]