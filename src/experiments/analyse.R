#
#ModelName,ScenarioName,nspike,model,it,ErrorDist
#data = read.table("NSpike_Control_modelXnspike.csv",header=TRUE,sep=",")
#data = read.table("NSpike_Scenarios_modelXnspike.csv",header=TRUE,sep=",")
#data$ModelName = as.factor(data$ModelName)
#data$ScenarioName = as.factor(data$ScenarioName)
#data$model = as.factor(data$model)
#data$nspike <- as.factor(data$nspike)
#attach(data)
#head(data)


#library(ggplot2)
#a <- ggplot(data,aes(x = nspike,y = ErrorDist,color = model))
#a <- a + geom_boxplot(outlier.size=.5)
#a <- a + facet_wrap(~ScenarioName)
#a <- a + ylim(0.025,0.075)
#a <- a + scale_color_grey() + theme_classic()
#a <- a + theme(text = element_text(size = 20))
#ggsave("plot_nspike.png", plot = a, width = 10, height = 10)



#data = read.table("NSpike_Control_modelXnspikeXdt.csv",header=TRUE,sep=",")
#data$ModelName = as.factor(data$ModelName)
#data$ScenarioName = as.factor(data$ScenarioName)
#data$model = as.factor(data$model)
#data$nspike <- as.factor(data$nspike)
#attach(data)
#head(data)
#
#
#library(ggplot2)
#a <- ggplot(data,aes(x = nspike,y = ErrorDist,color = model))
#a <- a + geom_boxplot(outlier.size=.5)
#a <- a + facet_wrap(~dt)
#a <- a + ylim(0.025,0.075)
#a <- a + scale_color_grey() + theme_classic()
#a <- a + theme(text = element_text(size = 20))
#ggsave("plot_nspike_dt.png", plot = a, width = 10, height = 10)
#
#library(ggplot2)
#data1 <- read.table("NSpike_prng_sequencexscenario_spike.csv",header=TRUE,sep=",")
#data2 <- read.table("NSpike_sequencexscenario_spike_period2.csv",header=TRUE,sep=",")
#data2$routerType <- "period2"
#
#data <- rbind(data1,data2)
#data$ScenarioName <- as.factor(data$ScenarioName)
#head(data)
#
#a <- ggplot(data,aes(x = ScenarioName,y = ErrorDist,color = routerType))
#a <- a + geom_boxplot()
#ggsave("nspike.png",plot=a,width=10,height=10)
#


#data1$ModelName <- as.factor(data1$ModelName)
#data1$routerType <- as.factor(data1$routerType)
#data1$nspike <- as.factor(data1$nspike)
#
#
#a <- ggplot(data1,aes(x = nspike,y = ErrorDist,color=routerType))
##a <- ggplot(data1,aes(x = Scenario,y = ErrorDist,color=routerType))
#a <- a + geom_boxplot()
#a <- a + ylim(0.025,0.075)
#ggsave("nspike.png",plot=a,width=10,height=10)

#rsdnf2 : the random bit are shared within a neuron (both exc and inh layer)
#library(ggplot2)
#data1 <- read.table("NSpike_rsdnf2Scenario_1spike.csv",header=TRUE,sep=",")
#data1$nspike = 1
#data2 <- read.table("NSpike_rsdnf2Scenario_20spike.csv",header=TRUE,sep=",")
#data2$nspike = 20
#head(data1)
#head(data2)
#data <- rbind(data1,data2)
#data$nspike <- as.factor(data$nspike)
#head(data)
#attach(data)
#
#a <- ggplot(data,aes(x = ScenarioName,y = ErrorDist,color=nspike))
#a <- a + geom_boxplot()
#ggsave("nspike.png",plot=a,width=10,height=10)
#
nbExp = 50
library(ggplot2)
data1 <- read.table("NSpike_prng_sequencexnspike_spike.csv",header=TRUE,sep=",")
data1 <- data1[data1$routerType != "sequence",]


data2 <- read.table("NSpike_controle_mixteXshort_nspike1_v2.csv",header=TRUE,sep=",")
stopifnot(nrow(data2)==2*nbExp)
data2$nspike = 1
data3 <- read.table("NSpike_controle_mixteXshort_nspike3_v2.csv",header=TRUE,sep=",")
data3$nspike = 3
data5 <- read.table("NSpike_controle_mixteXshort_nspike5_v2.csv",header=TRUE,sep=",")
data5$nspike = 5
data10 <- read.table("NSpike_controle_mixteXshort_nspike10_v2.csv",header=TRUE,sep=",")
data10$nspike = 10
data20 <- read.table("NSpike_controle_mixteXshort_nspike20_v2.csv",header=TRUE,sep=",")
data20$nspike = 20

#dataSeq5 <- read.table("NSpike_controle_mixteXsequence_nspike5.csv",header=TRUE,sep=",")
#dataSeq5$nspike <- 5
dataSeq10 <- read.table("NSpike_controle_mixteXsequence_nspike10.csv",header=TRUE,sep=",")
dataSeq10$nspike <- 10
dataSeq20 <- read.table("NSpike_controle_mixteXsequence_nspike20.csv",header=TRUE,sep=",")
dataSeq20$nspike <- 20

distrSeq5 <- read.table("NSpike_distr_sequence_nspike5.csv",header=TRUE,sep=",")
distrSeq5$nspike <- 5
#distrSeq10 <- read.table("NSpike_distr_sequence_nspike10.csv",header=TRUE,sep=",")
#distrSeq10$nspike <- 10
distrSeq20 <- read.table("NSpike_distr_sequence_nspike20.csv",header=TRUE,sep=",")
distrSeq20$nspike <- 20

dataControl <- rbind(data1,data2,data3,data5,data10,data20,
              #dataSeq5,
              dataSeq10,dataSeq20)
dataControl$ScenarioName = "ScenarioControl"
dataDistr <- rbind(distrSeq5,
                   #distrSeq10,
                   distrSeq20)
dataDistr$ScenarioName = "ScenarioDistracters"
dataDistr$routerType = "sequence"

prngxScenario <- read.table("NSpike_prng_sequencexscenario_spike.csv",header=TRUE,sep=",")
prngxScenario <- prngxScenario[prngxScenario$routerType != "sequence",]
prngxScenario$nspike = 20 #clkPeriod = 500
head(dataControl)
head(dataDistr)
head(prngxScenario)

data <- rbind(dataControl,dataDistr,prngxScenario)

data$routerType <- as.factor(data$routerType)
data$nspike <- as.factor(data$nspike)

#data <- data[data$ErrorDist < 0.16,]
dataControl <- data[data$ScenarioName == "ScenarioControl",]
a <-ggplot(dataControl,aes(x = routerType,y = ErrorDist,color=nspike))
a <- a + geom_boxplot()
a <- a + scale_color_grey() 
a <- a + theme_bw() + theme(plot.background = element_blank()) +
  xlab("Architecture") +
  ylab("Mean error distance")
ggsave("control_routerXnspike.png",plot=a,width=6,height=4)

dataDistr <- data[data$ScenarioName == "ScenarioDistracters",]
a <-ggplot(dataControl,aes(x = routerType,y = ErrorDist,color=nspike))
a <- a + geom_boxplot()
a <- a + scale_color_grey() 
a <- a + theme_bw() + theme(plot.background = element_blank()) +
  xlab("Architecture") +
  ylab("Mean error distance")
ggsave("distracters_routerXnspike.png",plot=a,width=6,height=4)

