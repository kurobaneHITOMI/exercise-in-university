#web
web_mat <- 
as.data.frame(cbind(c(0,1,1,0,0,0),
                    c(1,0,0,1,0,0),
                    c(1,0,0,1,0,0),
                    c(0,1,1,0,1,1),
                    c(0,0,0,1,0,1),
                    c(0,0,0,1,1,0)))

#parametre
r <- 0.8

#reward for the nth person
reward <- function(n,dec)
{
  value <- 0
  for(i in 1:length(web_mat[n,]))
  {
    if(web_mat[n,i] == 1)#if it's related
    {
      #1:cooperation,0:betray
      if(dec[n]==1 & dec[i]==1)
        value <- value + 1
      if(dec[n]==1 & dec[i]==0)
        value <- value + 1-r
      if(dec[n]==0 & dec[i]==1)
        value <- value + 1+r
      if(dec[n]==0 & dec[i]==0)
        value <- value + 0
    }
  }
  return(value)
}

nash <- function()
{
  #initialize decision
  decision <- round(runif(length(web_mat[1,]),0,1))
  print(decision)
  #anyone can change his decision
  mark <- 1
  while(mark != 0)
  {
    mark <- 0
    for(i in 1:length(web_mat[1,]))
    {
      decision[i] <- 1-decision[i]
      a <- reward(i,decision)#change
      decision[i] <- 1-decision[i]
      b <- reward(i,decision)#don't change
      
      if(a > b)
      {
        decision[i] <- 1-decision[i]
        mark <- mark + 1
      }
    }
  }
  print(decision)
}
nash()
