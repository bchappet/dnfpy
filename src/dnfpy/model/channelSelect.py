from dnfpy.core.map2D import Map2D


class ChannelSelect(Map2D):
        def _compute(self,map,channel):
                self._data = map[...,channel]
