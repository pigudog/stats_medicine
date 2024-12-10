library(meta)
#数据来源于<艾灸治疗脑卒中后尿失禁临床效果的Meta分析>
md = read.csv('rTMS.csv')
md = md[-4,]
mod = metacont(Experimental_total,Experimental_mean,Experimental_SD,
               Control_total,Control_mean,Control_SD,
               sm='SMD',
               studlab = `Study.Year`,data=md)
summary(mod) #总结并输出结果
funnel(mod)
forest(mod,col.square = "black",
       col.diamond = "black",
       col.diamond.lines = "black",
       hetstat = TRUE,leftcols = "studlab")
forest(metainf(mod), comb.fixed=TRUE)
library(ggplot2)
library(ggpubr)
library(tidyverse)
library(reshape2)
library(ggthemes)
md = read.csv('compare.csv')
md = md[-5,]
dt_long <- melt(md,
                measure.vars = c("Experimental_mean","Control_mean"),
                variable.name = "Study.Year",
                value.name = "value")
dt_long  = dt_long[,c(1,4,5)]
colnames(dt_long)= c("Year","group","value")
p<-ggplot(dt_long,aes(x=group,y=value,color=Year))+
  stat_boxplot(geom='errorbar',width=0.3,
               position=position_dodge(0.75))+
  geom_boxplot(position=position_dodge(0.75))+
  geom_jitter(mapping=aes(color=Year),width=0.0)+
  labs(x='Time',y='Count')+
  guides(color='none')+
  stat_compare_means(
    # comparisons=list(c("OJ","VC")),
    method="t.test",#t.test or wilcox.test
    paired=T,
    hide.ns=F,
    label='p.signif'  
    #"p.signif"(shows the significance levels),"p.format"(shows the formatted p value)
  )+
  theme_bw()
p

# 绘制散点图+配对连线
p1 <- ggplot(dt_long,aes(x=group,y=value,color=group))+
  geom_line(aes(group = Year),
            size = 0.5)+ #图层在下，就不会显示到圆心的连线
  geom_point(shape = 21,
             size = 3,
             stroke = 0.6,
             color = 'black')+
  scale_x_discrete(expand = c(-1.05, 0)) + # 坐标轴起始
  scale_fill_manual(values = c('#800040','#108080'))+ 
  geom_rangeframe() + # 坐标轴分离
  theme_tufte() +
  theme(legend.position = 'none',  # 标签字体等
        axis.text.y = element_text(size = 14,
                                   face = "bold"),
        axis.text.x = element_text(size =14,
                                   face = "bold"),
        axis.title.y = element_text(size = 15, 
                                    color = "black",
                                    face = "bold")) +
  labs(x = ' ', 
       y = 'Values')

p1

# 为了绘制原图的差异形式 手动计算p值
library(rstatix)
result = t_test(dt_long,value~group)  
head(result)
# > head(result)
# A tibble: 1 × 8
# .y.   group1            group2          n1    n2 statistic    df     p
# <chr> <chr>             <chr>        <int> <int>     <dbl> <dbl> <dbl>
#   1 value Experimental_mean Control_mean     4     4      2.67  4.93 0.045