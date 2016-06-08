from dnfpy.core.mapND import MapND


class SFAMap(MapND):
    def _compute(self,pot,tau,dt,m):
        self._data = self._data + dt/tau*(-self._data + m*pot)

