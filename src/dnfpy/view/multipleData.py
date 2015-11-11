
from dnfpy.core.mapND import MapND

class MultipleData(MapND):
        """
        The view will consider several data, they will be display with diferent color
        """

        def __init__(self,*args,**kwargs):
                super().__init__(*args,**kwargs)
                self.colors = ['red','green','blue','purple','cyan','black'] #default

        def addMaps(self,*maps):
                """
                Add a list of map to display
                """
                self.maps = maps
                names = [map.getName() for map in maps]
                children = {names[i]:maps[i] for i in range(len(maps))}
                self.addChildren(**children)

        def getViewData(self):
                """
                By default, return all children as a set
                """
                return [x.getData() for x in self.maps]

        def setColors(self,colors):
                self.colors = colors

        def getColors(self):
                return self.colors




