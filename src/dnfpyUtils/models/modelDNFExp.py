from dnfpyUtils.models.modelDNF import ModelDNF

class ModelDNFExp(ModelDNF):
    def initMaps(self,size=49,model="spike",activation="step",nbStep=0,
                 iExc=4.52,iInh=3.96,pExc=0.13,pInh=0.45,
                 alpha=10.,th=0.75,h=0
                 ):
        return super(ModelDNFExp,self).initMaps(size,model,activation,nbStep,
                        iExc=iExc,iInh=iInh,wExc=pExc,wInh=pInh,
                        lateral='doe',h=h,alpha=alpha,th=th)
