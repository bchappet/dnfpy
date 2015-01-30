class DnfContext(object):
    def __init__(self,*args):
        listParam = ["iExc","iInh","wExc","wInh","alpha","tau"]
        self.kwargs = {}
        for i in range(len(args)):
            self.kwargs[listParam[i]] = args[i]
        print self.kwargs


    def apply(self,model):
        model.getMap("DNF_kernel").setParamsRec(**self.kwargs)
        model.getMap("DNF").setParams(tau=self.kwargs["tau"])
