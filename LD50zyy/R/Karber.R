#' Title improved karber methods
#'
#' @param data
#' a dataframe
#' @return
#' @export
#'
Karber <- function(data){
  data
  Xm = log10(data[dim(data)[1],1])
  data$death_rate <- data[,2]/data[,3]
  sumP = sum(data$death_rate)
  I = log10(data[2,1]/data[1,1])
  LD_1 = Xm-I*(sumP-0.5)
  cat("LD50:")
  print(10^LD_1)
}

