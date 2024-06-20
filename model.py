
__all__ = [
    "Model"
]

class Model:
    def __init__(self, server):
        self.server = server
        self.state = server.state
        self.ctrl = server.controller
        self.updateCallback = {}

    def AddUpdataCallBack(self, key, fun):
        self.updateCallback[key] = fun
        
    def RemoveUpdateCallback(self, key):
        self.updateCallback.pop(key)

    def SignalUpdate(self):
        """
        数据更新时回调
        """
        for name, callBackFun in self.updateCallback.items():
            callBackFun()
