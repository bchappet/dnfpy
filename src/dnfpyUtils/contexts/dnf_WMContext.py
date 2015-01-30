class Dnf_WMContext(object):
    def __init__(self,**kwargs):
        self.paramDicts = {
            'iExc' : 2.0,
            'iInh' : 1.2,
            'wExc' : 0.06,
            'wInh' : 0.14,

            'iFEF->WM' : 3.4,
            'wFEF->WM' : 0.08,

            'iWM->FEF' : 1.8,
            'wWM->FEF' : 0.1,

            'iDNF->FEF' : 1.,
            'wDNF->FEF' : 0.1,

            'iINPUT->FEF' : 0.3,
            'wINPUT->FEF' : 0.1,
        }
        self.paramDicts.update(kwargs)
        print self.paramDicts


    def apply(self,model):
        model.getMap("FEF_kernel").setParamsRec(
            iExc=self.paramDicts['iExc'],
            iInh=self.paramDicts['iInh'],
            wExc=self.paramDicts['wExc'],
            wInh=self.paramDicts['wInh']
        )

        model.getMap("FEF->WM_kernel").setParamsRec(
            iExc=self.paramDicts['iFEF->WM'],
            wExc=self.paramDicts['wFEF->WM'])

        model.getMap("WM->FEF_kernel").setParamsRec(
            iExc=self.paramDicts['iWM->FEF'],
            wExc=self.paramDicts['wWM->FEF'])

        model.getMap("DNF->FEF_kernel").setParamsRec(
            iExc=self.paramDicts['iDNF->FEF'],
            wExc=self.paramDicts['wDNF->FEF'])

        model.getMap("INPUT->FEF_kernel").setParamsRec(
            iExc=self.paramDicts['iINPUT->FEF'],
            wExc=self.paramDicts['wINPUT->FEF'])
