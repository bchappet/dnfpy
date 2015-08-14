from dnfpy.core.mapND import MapND

class GainMap(MapND):
        def __init__(self,map,gain=1.0):
                super(GainMap,self).__init__(size=map.getSize(),dtype=map.getDtype(),name=map.name+"_gain",dt=map.getArg('dt'),gain=gain)
                self.addChildren(map=map)

        def _compute(self,map,gain):
                self._data = gain*map

