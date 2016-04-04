###################### Pairwise test####################
dataControl <- data[data$ScenarioName == "ScenarioControl",]


controlSpike1 <-dataControl[dataControl$nspike == 5,]
attach(controlSpike1)
#Box plot 
png('tmp1.png',width=800,height=600)
boxplot(controlSpike1$ErrorDist ~ controlSpike1$routerType)
dev.off()

png('tmp1o.png',width=800,height=600)
boxplot(controlSpike1$ErrorDist ~ controlSpike1$routerType,outline = FALSE)
dev.off()

#test for normality
png('tmp2.png')
qqnorm(ErrorDist)
qqline(ErrorDist)
dev.off()
#seems average
shapiro.test(ErrorDist)
#   Shapiro-Wilk normality test
#
#data:  ErrorDist
#W = 0.99105, p-value = 0.06489
#H0 almost rejected. H0 normal

#is it because of sequence?
seq <-controlSpike1[routerType == "sequenceShort",] 
shapiro.test(seq$ErrorDist)
#data:  seq$ErrorDist
#W = 0.92143, p-value = 0.002656 NOT NORMAL
others <-controlSpike1[routerType != "sequenceShort",] 
shapiro.test(others$ErrorDist)
#data:  others$ErrorDist
#W = 0.99071, p-value = 0.1124 NORMAL
#attach(others)


#check for heteroscedasticity
bartlett.test(ErrorDist ~ routerType)
#    Bartlett test of homogeneity of variances

#data:  ErrorDist by routerType
#Bartlett's K-squared = 15.11, df = 5, p-value = 0.009901
##H0 rejected H0:variance are the same

# Nonparametric alternative to Bartlett is called Fligner's test:
fligner.test(ErrorDist ~ routerType)
#
#    Fligner-Killeen test of homogeneity of variances

#data:  ErrorDist by routerType
#Fligner-Killeen:med chi-squared = 21.716, df = 5, p-value = 0.0005929
##H0 rejected H0:variance are the same


png('tmp3.png')
m = lm(ErrorDist ~ routerType)
plot(resid(m) ~ predict(m), ylab = "Residuals", xlab = "Group mean diversity")
dev.off()




#ANOVA
fit <- aov(ErrorDist ~ routerType)
summary(fit)
#             Df   Sum Sq   Mean Sq F value Pr(>F)    
#routerType    5 0.001568 3.135e-04   26.85 <2e-16 ***
#Residuals   294 0.003433 1.168e-05   
##H0 rejected H0: means are equal





#Non parametric
kruskal.test(ErrorDist ~ routerType)
pairwise.wilcox.test(ErrorDist, routerType, p.adj = "holm")

#relaxing variance equality
oneway.test(ErrorDist ~ routerType)
pairwise.t.test(ErrorDist,routerType,pool.sd=F)


