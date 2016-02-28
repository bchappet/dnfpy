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



data = read.table("NSpike_Control_modelXnspikeXdt.csv",header=TRUE,sep=",")
data$ModelName = as.factor(data$ModelName)
data$ScenarioName = as.factor(data$ScenarioName)
data$model = as.factor(data$model)
data$nspike <- as.factor(data$nspike)
attach(data)
head(data)


library(ggplot2)
a <- ggplot(data,aes(x = nspike,y = ErrorDist,color = model))
a <- a + geom_boxplot(outlier.size=.5)
a <- a + facet_wrap(~dt)
a <- a + ylim(0.025,0.075)
a <- a + scale_color_grey() + theme_classic()
a <- a + theme(text = element_text(size = 20))
ggsave("plot_nspike_dt.png", plot = a, width = 10, height = 10)
