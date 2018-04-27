
x <- seq(-3,4,by=0.1)
y <- 3*x^4-4*x^3-12*x^2
plot(x,y,type="l",col="red")
title(main="y = 3*x^4 - 4*x^3 - 12*x^2")
F <- expression(3*x^4-4*x^3-12*x^2)

f <- function(x)
{
  y <- 3*x^4-4*x^3-12*x^2
  return(y)
}

#parametre
a <- -10
b <- 10
e <- 0.01

glodensection <- function(a,b,e)
{
  t1 <- a+0.382*(b-a);
  t2 <- a +0.618*(b-a);
  f1 <- f(t1);
  f2 <- f(t2);
  while(abs(b-a)>e)
  {
    if(f1 > f2)
    {
      a <- t1
      t1 <- t2
      t2 <- a +0.618*(b-a)
      f1 <- f2
      f2 <- f(t2)
    }
    else
    {
      b <- t2
      t2 <- t1
      t1 <- a+0.382*(b-a)
      f2 <- f1
      f1 <- f(t1)
    }
  }
  tx <- (b+a)/2;
  fx <- f(tx)
  area <- c(a,b)
  print('the area is:')
  print(area)
  print('the xmin is:')
  print(tx)
  print('the fmin is:')
  print(fx)
}

glodensection(a,b,e)