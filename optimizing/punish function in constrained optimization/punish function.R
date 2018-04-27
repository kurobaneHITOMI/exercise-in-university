#parametre
eps <- 1e-06
mk <- 10
x0 <- c(2,2)
c <- 2
k <- 0
maxk <- 100
#target
f <- function(x)
{
  - x[1] + x[2]
}
#augmentation function
af <- function(x)
{
  (- x[1] + x[2]) + mk*((x[1]+x[2]-1)^2 + (max(0,-log(x[2])))^2)
}
#optimize
x1 <- x0
res <- optim(x0,af,method = "CG")
while((abs(f(x1)-f(res$par)) > eps) & (k <= maxk))
{
  x1 <- res$par
  mk <- c*mk
  res <- optim(res$par,af,method = "CG")
  print(k)
  print(res$par)
  print(f(res$par))
  print("========================================")
  k <- k+1
}







#parametre
eps <- 1e-06
rk <- 10
x0 <- c(2,2)
c <- 0.1
k <- 0
maxk <- 100
#target
f <- function(x)
{
  - x[1] + x[2]
}
#augmentation function
af <- function(x)
{
  (- x[1] + x[2]) + rk*(1/log(x[2])) + (1/(sqrt(rk)))*((x[1]+x[2]-1)^2)
}
#parametre
x1 <- x0
res <- optim(x0,af)
fx <- rep(0,100)
while((abs(f(x1)-f(res$par)) > eps) & (k <= maxk))
{
  x1 <- res$par
  rk <- c*rk
  res <- optim(res$par,af)
  fx[k+1] <- f(res$par)
  print(k)
  print(res$par)
  print(f(res$par))
  print("========================================")
  k <- k+1
}
plot(fx,type = "l")