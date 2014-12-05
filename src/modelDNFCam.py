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
