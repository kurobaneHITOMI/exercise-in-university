
x <- seq(-2,3,by=0.1)
y <- 3*x^4-4*x^3-12*x^2
plot(x,y,type="l",col="red")
title(main="y in red, y' in green, y'' in blue")
F0 <- expression(3*x^4-4*x^3-12*x^2)
F1 <- D(F0,'x')
F2 <- D(F1,'x')

points(x,eval(F1),type="l",col="green")
points(x,eval(F2),type="l",col="blue")

#derivative 0\1\2
f0 <- function(x)
{
  f <- 3*x^4-4*x^3-12*x^2
  return(f)
}

f1 <- function(x)
{
  f <- D(F0,'x')
  x <- x
  return(eval(f))
}

f2 <- function(x)
{
  f <- D(D(F0,'x'),'x')
  x <- x
  return(eval(f))
}

#parametre
a <- -10
b <- 10
e <- 0.01
#original newton
nt <- function(t0)
{
  t <- t0 - f1(t0)/f2(t0)
  while(abs(t-t0)>e)
  {
    t0 <- t
    t <- t0 - f1(t0)/f2(t0)
  }
  return(t0)
}
#random newton
newton1 <- function()
{

  ymin <- 0
  xmin <- 0
  for(i in 1:10)
  { 
    x <- nt(runif(1,a,b))
    y <- f0(x)
    if(y < ymin)
    {
      ymin <- y
      xmin <- x
    }
  }
  z <- c(xmin,ymin)
  sprintf("%.3f",z)
}
newton1()

