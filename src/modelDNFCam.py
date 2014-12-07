from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.mapDNF import MapDNF


class ModelDNFCam(Model,Renderable):

    def initMaps(self,size):
        #Create maps
        self.webcam = WebcamMap("Webcam",size,numDevice=0)
        self.color_select = ImageColorSelection("ColorSelect",size)
        self.field = MapDNF("DNF",size)
        #Link maps
        self.color_select.addChildren(image=self.webcam)
        self.aff = self.color_select
        self.field.addChildren(aff=self.aff)
        #return the root
        return self.field

    def getArrays(self):
        ret =  [
                self.webcam,
                self.aff,
                self.field
        ]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        if mapName == "Webcam":
            hsv = self.webcam.getData()[y,x]
            colorVal = hsv[0]
            satuVal = hsv[1]
            satLow = satuVal - 60
            satHigh = satuVal + 60
            self.color_select.setArg(colorVal=colorVal,satLow=satLow,satHigh=satHigh)

