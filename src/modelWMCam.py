from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.convolution import Convolution
import dnfpy.core.utils as utils
from dnfpy.model.mapDNF import MapDNF
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords


class ModelWMCam(Model,Renderable):

    def onClick(self,x,y):
        self.gauss.setParams(centerX=x,centerY=y,intensity=1.)


    def initMaps(self,size):
        model = 'spike'
        dt = 0.6
        wrap = True
        #Input
        self.webcam = WebcamMap("Webcam",size,dt=dt,numDevice=0)
        self.color_select = ImageColorSelection("Color Select",size,dt=dt,thresh=5)

        mapSize = 0.3
        #Excitatory Memory
        self.fieldE = MapDNF("ExcitatoryField",size,dt=dt,mapSize=mapSize,model=model,
                             iExc=2.2,iInh=1.5,
                             wExc=0.1/2.,wInh=0.2/2.)
        #Inhibition memory
        self.fieldI = MapDNF("InhibitoryField",size,dt=dt,mapSize=mapSize,model=model,
                             iExc=2.2,iInh=1.5,
                             wExc=0.1/2.,wInh=0.2/2.,
                             h=-0.6)
        #artificial gaussian to bost inhbitory
        center = (size-1)/2
        self.gauss = FuncMap2D(utils.gauss2d,"ArtificialOnClickGaussian",
                               size=size,dt=dt,wrap=wrap,
                        intensity=0.,width=0.1*size,centerX=center,centerY=center)
        #TODO add unlimited amount of input to field
        self.add_gauss_and_input = FuncWithoutKeywords(utils.sumArrays,
                    "InputAndArtificialGaussian",size=size,dt=dt)
        self.add_gauss_and_input.addChildren(gauss=self.gauss,input=self.color_select)




        #Exc - Inh
        self.substract = FuncMap2D(utils.subArrays,"Exc - Inh",size,dt=0.1)

        #Neural field selection
        self.field = MapDNF("DNF",size)

        #Link maps

        self.color_select.addChildren(image=self.webcam)
        self.aff = self.color_select

        #Excitatory
        self.fieldE.addChildren(aff=self.aff)

        #Inhibitory
        self.fieldI.addChildren(aff=self.add_gauss_and_input)

        #Exc - Inh
        self.substract.addChildren(a = self.fieldE.getActivation(),
                                   b = self.fieldI.getActivation())
        #Neural field

        self.field.addChildren(aff=self.substract)

        #return the root
        return self.field

    def getArrays(self):
        ret =  [
                        self.webcam,
                        self.aff,
                        self.substract,
                        self.gauss,
                        self.add_gauss_and_input,
                        self.fieldI,
                        self.fieldE,
                        self.field,
        ]
        ret.extend(self.fieldI.getArrays())
        #ret.extend(self.fieldE.getArrays())
        #ret.extend(self.field.getArrays())
        return ret

    def onlick(self,x,y):
        pass


