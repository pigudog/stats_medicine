test_data = data.frame('con' = c(110.8,147.7,196.9,262.5,350.0),'death' = c(0,5,6,8,10), 'total' = c(10,10,10,10,10))

print(test_data,row.names=F)

library(MASS)
source("./R/Bliss.R")
LD_cal(test_data)

source("./R/Karber.R")
Karber(test_data)
