library(ggplot2)
data = read.table("exp_gen_random_all.csv",sep=",",header=T)

data$routerType <- as.factor(data$routerType)
data$routerType <- factor(data$routerType,levels=c("prng","shared","sequenceShort","sequence","sequenceShortMixte","sequenceMixte"))
data$nspike <- as.factor(data$nspike)
data$ScenarioName <- as.factor(data$ScenarioName)
summary(data)
attach(data)








dataControl <- data[data$ScenarioName == "ScenarioControl",]
dataControl <- dataControl[dataControl$ErrorDist < 0.06,]
a <-ggplot(dataControl,aes(x = nspike,y = ErrorDist,fill=routerType))
a <- a + geom_boxplot(outlier.shape=NA)
a <- a + scale_fill_manual(
                   values=c("#ffffff","#dddddd","#bbbbbb","#999999","#777777","#555555"),
                   limits=c("prng","shared","sequenceShort","sequence","sequenceShortMixte","sequenceMixte"),
                   breaks=c("prng","shared","sequenceShort","sequence","sequenceShortMixte","sequenceMixte"),
                   labels=c("Control", "shared", "short","long","shrtOpen","longOpen"))
#a <- a + scale_fill_grey()
#a <- a + scale_fill_grey(start = 0, end = .9)
a <- a + theme_bw() + theme(plot.background = element_blank()) 
a <- a + xlab("Number of sub-spike") + ylab("Mean error distance")
 
ggsave("routerXnspike_control.png",plot=a,width=6,height=3,dpi=1200)



