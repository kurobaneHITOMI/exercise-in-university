
x <- seq(-2,3,by=0.1)
y <- 3*x^4-4*x^3-12*x^2
plot(x,y,type="l",col="red")
title(main="y in red, y' in green, y'' in blue")
F0 <- expression(3*x^4-4*x^3-12*x^2)


f <- function(x)
{
  y <- 3*x^4-4*x^3-12*x^2
  return(y)
}

#parametre
e <- 0.001
t1 <- 0
t2 <- 3
t0 <- (t1+t2)/2
insertion <- function()
{
  t <- ((t0^2-t2^2)*f(t1)+(t2^2-t1^2)*f(t0)+(t1^2-t0^2)*f(t2))/(2*((t0-t2)*f(t1)+(t2-t1)*f(t0)+(t1-t0)*f(t2)))
  return(t)
}

#second_insertion
second_insertion <- function()
{
  tv <- insertion()
  while(abs(t0-tv)>e)
  {
    if(tv > t0)
    {
      if(f(tv) <= f(t0))
      {
        t1 <- t0
        t0 <- tv
      }
      else
      {
        t2 <- tv
      }
    }
    else
    {
      if(f(t1) <= f(tv))
      {
        t1 <- tv
      }
      else
      {
        t2 <- t0
        t0 <- tv
      }
    }
    tv <- insertion()
  }
  print(tv)
  print(f(tv))
}
second_insertion()