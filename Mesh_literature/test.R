install.packages("installr")
library(installr)
updateR()


remotes::install_github("elizagrames/litsearchr", ref="main")
devtools::install_github("DaXuanGarden/DXMeSH")

install.packages("vctrs")
.libPaths("D:/Download/R-4.4.0/library/")
install.packages("vctrs")
library(DXMeSH)
library(ggraph)
source("utools.R")
get_mesh("search.csv")
