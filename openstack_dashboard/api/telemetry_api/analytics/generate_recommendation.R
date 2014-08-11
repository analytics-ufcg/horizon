#funcao de recomendacao ##############################################################################
recommendation <- function(data){
  probability = c(0.5, 0.6, 0.7, 0.8, 0.9, 1)
  limiar = 1 - 0.95
  recommendationFlavour <- data.frame(recommendation = c(), lose = c(), violation = c())
  one = vector()
  two = vector()
  three = vector()
  four = vector()
  five = vector()
  six = vector()
  core_util <- data
  core_util$CPU_UTIL <- core_util$Cores * (core_util$CPU_UTIL/100)
  
  for(vm in unique(core_util$VM)){
    selection <- subset(core_util, VM == vm)
    values <- quantile(selection$CPU_UTIL, probs = probability)
    position = length(one)
    one[position+1] = values[1]
    two[position+1] = values[2]
    three[position+1] = values[3]
    four[position+1] = values[4]
    five[position+1] = values[5]
    six[position+1] = values[6]
  }
  
  recOne <- processRec(one)
  recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recOne, limiar))
    
  recTwo <- processRec(two)
  if(differentRec(recTwo, recOne)){
    recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recTwo, limiar))
  }
  
  recThree <- processRec(three)
  if(differentRec(recThree, recOne) & differentRec(recThree, recTwo)){
    recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recThree, limiar))
  }
  
  recFour <- processRec(four)
  if(differentRec(recFour, recOne) & differentRec(recFour, recTwo) & differentRec(recFour, recThree)){
    recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recFour, limiar))
  }
  
  recFive <- processRec(five)
  if(differentRec(recFive, recOne) & differentRec(recFive, recTwo) & differentRec(recFive, recThree) & differentRec(recFive, recFour)){
    recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recFive, limiar))
  }
  
  recSix <- processRec(six)
  if(differentRec(recSix, recOne) & differentRec(recSix, recTwo) & differentRec(recSix, recThree) & differentRec(recSix, recFour) & differentRec(recSix, recFive)){
    recommendationFlavour <- rbind(recommendationFlavour, calcMetrics(core_util, recSix, limiar))
  }
  
  recommendationFlavour
}
######################################################################################################


#funcoes auxiliares ##################################################################################
processRec <- function(input){
  tb <- table(input)
  flavours <- names(tb[order(tb, decreasing = TRUE)])
  flavours <- ceiling(as.numeric(flavours))
  recommend = vector()
  for(value in flavours){
    if(!(value %in% recommend)){
      recommend[length(recommend) + 1] = value
    }
  }
  sort(recommend, decreasing = FALSE)
}

# retorna true se os vetores forem diferentes e false se forem iguais
differentRec <- function(vectorOne, vectorTwo){
  out = FALSE
  if(length(vectorOne)!=length(vectorTwo)){
    out = TRUE
  }else{
    for(value in vectorOne){
      if(!(value %in% vectorTwo)){
        out = TRUE
        break
      }
    }
  }
  out
}

#calcula o lose, violation de acordo com o limiar
calcMetrics <- function(data, recommendation, limiar){
  flavours = "Core"
  lose = vector()
  violation = 0
  for(i in 1:length(recommendation)){
    if(i==1){
      selection <- subset(data, CPU_UTIL < recommendation[i] - recommendation[i]*limiar)
      if(length(selection[,1]) != 0){
        lose[(length(lose)+1):(length(lose)+length(selection$CPU_UTIL))] = (recommendation[i] - selection$CPU_UTIL)/recommendation[i] 
        flavours <- paste(flavours, recommendation[i], sep=":")
      }
    }else{
      selection <- subset(data, CPU_UTIL < recommendation[i] - recommendation[i]*limiar & CPU_UTIL > recommendation[i-1] - recommendation[i-1]*limiar)
      if(length(selection[,1]) != 0){
        lose[(length(lose)+1):(length(lose)+length(selection$CPU_UTIL))] = (recommendation[i] - selection$CPU_UTIL)/recommendation[i]
        flavours <- paste(flavours, recommendation[i], sep=":")
      }
    }
    
    
    
    if(i == length(recommendation)){
      selection <- subset(data, CPU_UTIL >= recommendation[i] - recommendation[i]*limiar)
      violation = length(selection[,1])/length(data[,1])
      if(length(selection[,1]) != 0){
          lose[(length(lose)+1):(length(lose)+length(selection$CPU_UTIL))] = (recommendation[i] - selection$CPU_UTIL)/recommendation[i]
      }
    }
  }
  
  lose = lose * 100
  violation = round(violation * 100, 2)
  lose.temp = round(ic.m(lose), 2)
  lose.temp = paste("{", lose.temp[1], "-",lose.temp[2], "}", sep="")
  lose = paste(round(mean(lose), 2), lose.temp, sep = ":")
  
  out <- data.frame(recommendation = flavours, lose = lose, violation = violation)
}
######################################################################################################


#calcula intervalo de confianca para a media #########################################################
ic.m <- function(x, conf = 0.95){
    n <- length(x)
    media <- mean(x)
    variancia <- var(x)
    quantis <- qt(c((1-conf)/2, 1 - (1-conf)/2), df = n-1)
    ic <- media + quantis * sqrt(variancia/n)
    return(ic)
}
######################################################################################################


#carregando dados ####################################################################################
args <- commandArgs(trailingOnly = TRUE)
data <- read.csv(args[1])
######################################################################################################


#gerando os flavours #################################################################################
out <- recommendation(data)
######################################################################################################

#print(out)

#salvando em arquivo a saida #########################################################################
write.csv(out, "flavors.csv", row.names=F)
######################################################################################################
