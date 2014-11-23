from map2D import Map2D

class FieldMap(Map2D):
    def compute(self):
        super(FieldMap,self).compute()

        model = self.globalRealParams['model']
        lat = self.children['lateral'].getData()
        aff = self.children['afferent'].getData()

        if model == 'cnft':
            self.data = self.data + self.globalRealParams['dt']/self.globalRealParams['tau']*(-self.data + self.globalRealParams['h'] + aff + lat)
        elif model == 'spike':
            tau = self.globalRealParams['tau']
            th = self.globalRealParams['threshold']
            self.data = np.where(self.data > th,0,self.data) # if x > th => x = 0
            self.data = self.data + self.globalRealParams['dt']/tau*(-self.data + self.globalRealParams['h'] + aff ) +  1/tau*lat
        else:
            print "Invalid model option : " + model

