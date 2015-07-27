class NSpikeContext(object):
    def __init__(self,*args):
        listParam = ["iExc","iInh","pExc","pInh"]#,"alpha","tau"]
        self.kwargs = {}
        for i in range(len(args)):
            self.kwargs[listParam[i]] = args[i]
        print self.kwargs


    def apply(self,model):
        model.getMap("DNF_spikePropag.").setParamsRec(**self.kwargs)
        #model.getMap("DNF").setParams(tau=self.kwargs["tau"])
