from constantsymbol import Constant
from model import Model
import os
from pathlib import Path

__all__ = [
    "LeftModel"
]

class LeftModel(Model):
    def __init__(self, server, dir):
        super().__init__(server)
        self.dir = dir

        self.infoGroup = {}
        self.UpdateModel()

    def UpdateModel(self):
        """
        读取dir路径下的文件并更新
        """
        self.infoGroup.clear()
        for root, dirs, files in os.walk(self.dir):
            # 只遍历根目录
            if root != str(self.dir):
                break

            for file in files:
                path = self.dir / file

                # 文件名
                fileName = file.split('.')[0]

                # 文件中的字符串列表
                resFile = open(path.absolute(),
                    mode ='r',
                    encoding = 'gb2312')

                strList = resFile.readlines()
                resFile.close()

                # 保存
                self.infoGroup[fileName] = strList

        # 更新信号
        self.SignalUpdate()