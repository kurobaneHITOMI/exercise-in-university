#s0 - start   sg - target
s0 <- matrix(c(2,8,3,1,4,0,7,6,5),byrow=T, nrow=3)
sg <- matrix(c(1,2,3,8,0,4,7,6,5),byrow=T, nrow=3)
ss <- matrix(c(0,0,0,0,0,0,0,0,0),byrow=T, nrow=3)
library(rlist)


#if it's target
is_equal <- function(snlist,s)
{
  for(i in 1:3)
  {
    for(j in 1:3)
    {
      if(snlist[[1]][i,j] != s[i,j])
        return(FALSE)
    }
  }
  return(TRUE)
}


#inspiration
hn <- function(sn)
{
  hn <- 0
  for(i in 1:3)
  {
    for(j in 1:3)
    {
      if(sn[i,j] != sg[i,j])
        hn <- hn + 1
    }
  }
  return(hn)
}


#location of zero
findzero <- function(sn)
{
  ij <- c(0,0)
  for(i in 1:3)
  {
    for(j in 1:3)
    {
      if(sn[i,j] == 0)
        ij <- c(i,j)
    }
  }
  return(ij)
}


# move zero left
moveleft <- function(sn)
{
  ij <- findzero(sn)
  if(ij[2] != 1)
  {
    t <- sn[ij[1],ij[2]]
    sn[ij[1],ij[2]] <- sn[ij[1],ij[2]-1]
    sn[ij[1],ij[2]-1] <- t
  }
  return(sn)
}
# move zero right
moveright <- function(sn)
{
  ij <- findzero(sn)
  if(ij[2] != 3)
  {
    t <- sn[ij[1],ij[2]]
    sn[ij[1],ij[2]] <- sn[ij[1],ij[2]+1]
    sn[ij[1],ij[2]+1] <- t
  }
  return(sn)
}
# move zero up
moveup <- function(sn)
{
  ij <- findzero(sn)
  if(ij[1] != 1)
  {
    t <- sn[ij[1],ij[2]]
    sn[ij[1],ij[2]] <- sn[ij[1]-1,ij[2]]
    sn[ij[1]-1,ij[2]] <- t
  }
  return(sn)
}
# move zero down
movedown <- function(sn)
{
  ij <- findzero(sn)
  if(ij[1] != 3)
  {
    t <- sn[ij[1],ij[2]]
    sn[ij[1],ij[2]] <- sn[ij[1]+1,ij[2]]
    sn[ij[1]+1,ij[2]] <- t
  }
  return(sn)
}

#open list and closed list
openlist <- list(list(s0, h = hn(s0),father = s0))
closedlist <- list(list(ss, h = hn(ss),father = ss))

#add or delete s in a list
add_list <- function(listx,snlist)
{
  listx <- c(listx,list(snlist))
  return(listx)
}
delete_list <- function(listx,sn)
{
  i <- 1
  while(!is_equal(listx[[1]],sn))
    i <- i+1
  listx[[i]] <- NULL
  return(listx)
}

#if sn in listx
search_list <- function(listx,sn)
{
  if(length(listx) == 0)
    return(FALSE)
  else
  {
    i <- 0
    while(i != length(listx))
    {
      if(is_equal(listx[[i+1]],sn))
        return(TRUE)
      else
        i <- i+1
    }
    return(FALSE)
  }
}

#sort the list by hn
sortlist <- function(listx)
{
  listx <- list.sort(listx,h)
  return(listx)
}

#extend node
extension <- function(snlist,listx)
{
  sn1 <- moveup(snlist[[1]])
  sn1 <- list(sn1, h = hn(sn1),father = snlist[[1]])
  if((!is_equal(sn1,snlist$father))  & (!search_list(closedlist,sn1[[1]])) & (!search_list(openlist,sn1[[1]])))
    listx <- add_list(listx,sn1)
  
  sn2 <- movedown(snlist[[1]])
  sn2 <- list(sn2, h = hn(sn2),father = snlist[[1]])
  if((!is_equal(sn2,snlist$father))  & (!search_list(closedlist,sn2[[1]])) & (!search_list(openlist,sn2[[1]])))
    listx <- add_list(listx,sn2)
  
  sn3 <- moveright(snlist[[1]])
  sn3 <- list(sn3, h = hn(sn3),father = snlist[[1]])
  if((!is_equal(sn3,snlist$father))  & (!search_list(closedlist,sn3[[1]])) & (!search_list(openlist,sn3[[1]])))
    listx <- add_list(listx,sn3)
  
  sn4 <- moveleft(snlist[[1]])
  sn4 <- list(sn4, h = hn(sn4),father = snlist[[1]])
  if((!is_equal(sn4,snlist$father))  & (!search_list(closedlist,sn4[[1]])) & (!search_list(openlist,sn4[[1]])))
    listx <- add_list(listx,sn4)
  return(listx)
}

#####################################################################################################
A_star <- function()
{
  print("??ʼ?ڵ?")
  print(s0)
  print("Ŀ???ڵ?")
  print(sg)  
  print("==================== START ====================")
  i <- 0
  
  while(length(openlist)!=0 & i<1000)
  {
    openlist <- sortlist(openlist)
    
    if(is_equal(openlist[[1]],sg))
    {
      print("==================== GAME OVER ====================")
      print(sg)
      break()
    }
    else
    {
      print(openlist[[1]][[1]])
      sl <- openlist[[1]]
      closedlist <- add_list(closedlist,openlist[[1]])
      openlist <- delete_list(openlist,sl[[1]])
      openlist <- extension(sl,openlist)
      i <- i+1
    }
    if(i == 1000)
      print("======= Have no solution ========")
  }
  
}
A_star()