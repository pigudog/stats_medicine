library(tidyverse)
library(readxl)
K_concentration <- read_excel("K_concentration.xlsx")
K_concentration = K_concentration[-1,]
head(K_concentration,10)

colnames(K_concentration) = c("treat","pheno","before","time","concentration")                          
K_concentration$treat=c(1:4)
K_concentration$group=1
K_concentration
#加上折线：
ggplot(K_concentration,
       aes(x = treat,y=concentration,
       color=group))+
  geom_point(size=4)+
  geom_line(position = position_dodge(0.1),cex=1.3)+
  geom_text(aes(label = concentration), size = 3,vjust = -3,show.legend = TRUE)
