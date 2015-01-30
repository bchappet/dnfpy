"""
    Interface view
"""
class View():
        def setRunner(self,runner):
                """
                Set runner
                """
                pass

        def update(self):
                """Signal that the model changed"""
                pass

        def updateParams(self,mapName):
                """Signal that the params of the map changed"""
                pass



