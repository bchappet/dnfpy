"""
    Interface view
"""
class View():
        def getParamsDict(self):
                pass
        def updateParamsDict(self,paramsDict):
                pass
        def setRunner(self,runner):
                """
                Set runner
                """
                pass

        def update(self):
                """Signal that the model changed"""
                pass


