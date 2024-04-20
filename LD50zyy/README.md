---
title: wechat2-LD50
categories:
  - medical
author: pigudogzyy
tags:
  - R
date: 2023-10-05
---
# Intro
This R package is used to calculate LD50
# Download
You can install the latest version of LD50zyy from GitHub with:

```r
if (!require("devtools", quietly = TRUE)) {
  install.packages("devtools")
}
devtools::install_github("pigudog/LD50zyy")
```

# 1. Bliss for LD50
include three functions
- `ctl`: used for control
	- Bliss methods need several precondition
	- If death rate in control group < 0.05, no correction is needed;
	- if death rate between 0.05 ~ 0.2, using Abbott fomula to adjust the assay;
	- if death rate > 0.2, invalid assay. Program will stop! Private function in LD50 package.
- `LDx`: used to infer LD50 and coresponding CI
- `LD_cal`: used to calculate LD50
	- you need to input a dataframe with three variables, with concentration, the number of death, and total number of experimental subject

## 1.1 Test
```r
test_data = data.frame('con' = c(110.8,147.7,196.9,262.5,350.0),'death' = c(0,5,6,8,10), 'total' = c(10,10,10,10,10))

print(test_data,row.names=F)
```
![](wechat2/Pasted%20image%2020231006201759.png)


```r
> LD_cal(test_data)
[1] Control OK!

[2] Summary of Model: 
$coefficients
             Estimate Std. Error   z value  Pr(>|z|)
(Intercept) -7.235112   5.432252 -1.331881 0.1828994
log_c        3.310995   2.374751  1.394249 0.1632424


[3] Chi-square test for goodness of fit:
 Chi_square df  P_value
  0.1121896  1 0.737665

[4] Estimate of LD50-LD99: 
     estimate       lci       uci
LD50 153.1714  96.75917  242.4730
LD90 373.4540 139.57240  999.2514
LD95 480.7985 127.84695 1808.1558
LD99 772.3084 106.92892 5578.1004
```

## 1.2 annotation
we must understand the details of the major functions in Bliss
- we used probability unit to analysis death rate
	- the y is ajusted death rate
	- the x is log(concentration)
- If the P-value of the Chi-square distribution test result is greater than 0.05, the hypothesis that each point deviates from the straight line is not significant
# 2. Karber 
Karber method was proposed by Karber in 1931, improved by Finney, improved by Gu Hanyi, and further improved by Professor Sun Ruiyuan in 1963. 

The improved calculation method was called the point slope method or Sun's method, and the number of death rates excluding 0% and 100% was increased. 

The obtained LD50 and all related parameters are similar to the normal probability unit method. 

The principle of Kaber test design is as follows: 
- the dose of each group should be proportionally graded; 
- The number of animals in each group is equal: roughly half of the groups have animal mortality between 10% and 50%, the other half is between 50% and 100%, and it is best to have 0 and 100% dose groups.
```r
> Karber(test_data)
LD50:[1] 175.57
```
